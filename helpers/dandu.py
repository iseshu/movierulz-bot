import requests
import time
from .jst import convert_bytes,convert_seconds_to_eta,generate_progress_bar


tex = '''
**📥 Downloading To Server**
`{}`
`Percentage` : `{}%`
`Total` : `{}`
`Downloaded` : `{}`
`Remaining` : `{}`
`Speed` : `{}/s`
`ETA` : `{}`
'''

async def download(message,url: str) -> None:
    r = requests.head(url, allow_redirects=True)
    file_size = int(r.headers.get('content-length', 0))
    r = requests.get(url, stream=True)
    start_time = time.time()
    elapsed_time = time.time()
    downloaded_size = 0
    with open("video.mkv", 'wb') as f:
        for chunk in r.iter_content(chunk_size=2048):
            if chunk:
                f.write(chunk)
                downloaded_size += len(chunk)
                if time.time() - elapsed_time > 5:
                    elapsed_time = time.time()
                    speed = downloaded_size / (time.time() - start_time)
                    eta = (file_size - downloaded_size) / speed if speed > 0 else 0
                    percent = f"{(downloaded_size / file_size) * 100:.2f}"
                    text = tex.format(generate_progress_bar((downloaded_size / file_size) * 100,10),percent, convert_bytes(file_size), convert_bytes(downloaded_size), convert_bytes(file_size - downloaded_size), convert_bytes(speed), convert_seconds_to_eta(eta))
                    await message.edit(text)
utex = '''
** 📤 Uploading to Telegram**
`{}`
`Percentage` : `{}%`
`Total` : `{}`
`Uploaded` : `{}`
`Remaining` : `{}`
`Speed` : `{}/s`
`ETA` : `{}`
'''

elapsed_time = 0
async def uploadtg(current,total,message,start_time):
    percent = f"{(current / total) * 100:.2f}"
    global elapsed_time
    if time.time()-elapsed_time > 5:
        speed = current / (time.time() - start_time)
        eta = (total - current) / speed if speed > 0 else 0
        text = utex.format(generate_progress_bar((current / total) * 100,10),percent, convert_bytes(total), convert_bytes(current), convert_bytes(total - current), convert_bytes(speed), convert_seconds_to_eta(eta))
        await message.edit(text)
        elapsed_time = time.time()
        
