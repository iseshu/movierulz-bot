from pyrogram import Client, filters
from pyrogram.types import Message
from config import Config
import os
config = Config()
plugins = dict(
    root="plugins"
)

bot = Client("my_bot",
             api_id=config.api_id,
             api_hash=config.api_hash,
             bot_token=config.bot_token,
            plugins=plugins
             )




if __name__ == '__main__':
    os.mkdir("ss") if not os.path.isdir("ss") else None
    bot.run()