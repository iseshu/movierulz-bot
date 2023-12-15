from config import Config
import imgbbpy
config = Config()
client = imgbbpy.SyncClient(config.imgbb_key)

url = "https://api.imgbb.com/1/upload"
def store_image(image):
    if image.startswith("http"):
        image = client.upload(url=image)
    else:
        image = client.upload(file=image)
    return image.url