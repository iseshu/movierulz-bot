from os import environ

class Config:
    api_id = int(environ.get('API_ID'))
    api_hash = str(environ.get('API_HASH'))
    bot_token = str(environ.get('BOT_TOKEN'))
    seedr_username = str(environ.get('SEEDR_USERNAME'))
    seedr_password = str(environ.get('SEEDR_PASSWORD'))
    onwer_id = int(environ.get('ONWER_ID'))
    channel_id = int(environ.get('CHANNEL_ID'))
    imgbb_key = str(environ.get('IMGBB_KEY'))
    mongodb_uri = str(environ.get('MONGODB_URI'))
