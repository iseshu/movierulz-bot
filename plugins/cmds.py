from pyrogram import Client, filters
from pyrogram.types import Message
from helpers.jst import get_torrents
from helpers.dandu import download,uploadtg
from helpers.sedr import deleteAll, upload_torrent,respose,select_File
from helpers.ssgen import screenshots
from helpers.img import store_image
from helpers.db import Database
from config import Config
import time,os,re
db = Database()
config = Config()
@Client.on_message(filters.command("start"))
async def start(client, message):
    await message.reply_text("Hello! Sir I'm working")

@Client.on_message(filters.regex(r"https?://[^\s]+")&filters.chat(config.onwer_id))
async def link_handler(client, message):
        link = message.matches[0].group(0)
        ss = True
        error_text  = ""
        title, image, description, torrents = await get_torrents(link)
        data = {}
        data['title'] = title
        data['schema'] = link.split("/")[-1]
        data['description'] = description
        ims= await client.send_photo(chat_id=config.channel_id,photo=image, caption=f"<b>**{title}**</b>\n\n`{description}`")
        data['image'] = {"link":store_image(image),"file_id":ims.photo.file_id,"file_unique_id":ims.photo.file_unique_id}
        data['id'] = ims.id
        data['files'] = []
        data['screenshots'] = []
        msg = await client.send_message(config.channel_id,"Admin Uploading the video to telegram wait for some time")
        time.sleep(3)
        rmsg = await message.reply_text("Uploading [{}]({}) to telegram \n[Progress]({})".format(title,
                                                                                           f"https://t.me/c/{str(config.channel_id).replace('-100','')}/{ims.id}",
                                                                                           f"https://t.me/c/{str(config.channel_id).replace('-100','')}/{msg.id}"))
        torrents = torrents[::-1]
        for torrent in torrents:
            uri = torrent['magnet']
            deleteAll()
            upload_torrent(uri)
            time.sleep(60)
            try:
                try:
                    file_name,url = select_File(respose())
                except:
                    time.sleep(90)
                    file_name,url = select_File(respose())
                file_name = re.sub(r'^.*?-', '', file_name).strip()
                await download(msg,url)
                if ss:
                    screen = await screenshots(client)
                    data['screenshots'].append(screen)
                    ss = False
                start_time = time.time()
                doc = await client.send_document(document="video.mkv",thumb="thumb.jpg",chat_id=config.channel_id,caption=file_name,file_name=file_name,progress=uploadtg,progress_args=(msg,start_time))
                os.remove('video.mkv')
                data['files'].append({"file_id":doc.document.file_id,"file_unique_id":doc.document.file_unique_id,"file_name":file_name,"file_size":doc.document.file_size})
                time.sleep(3)
            except Exception as e:
                error_text+=f"`{e}`\n"
                continue
        await msg.delete()
        time.sleep(3)
        if data['files'] == []:
            await rmsg.edit_text("Enable to upload the video to telegram")
        else:
            db.insert(data)
        if error_text !="":
            time.sleep(3)
            lk = "https://t.me/c/"+str(config.channel_id).replace('-100','')+f"/{ims.id}"
            await rmsg.edit_text(config.onwer_id,"Error at [{}]({})\n{}".format(title,lk,error_text))