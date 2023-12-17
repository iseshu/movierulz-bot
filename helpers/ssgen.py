import subprocess
import json
import os
import imageio
from config import Config
from .img import store_image
from pyrogram.types import InputMediaPhoto
config = Config()
def capture_frame(video_path, timestamp, output_filename):
    vid = imageio.get_reader(video_path, 'ffmpeg')
    frame_num = int(vid.get_meta_data()['fps'] * timestamp)
    frame = vid.get_data(frame_num)
    imageio.imwrite(output_filename, frame)

def get_duration(input_filename):
    command = ["ffprobe", "-v", "quiet", "-print_format", "json", "-show_format", "-show_streams", input_filename]
    output = subprocess.Popen(command, stdout=subprocess.PIPE).communicate()[0]
    data = json.loads(output)
    duration = float(data["format"]["duration"])
    return duration

def seconds_to_hms(seconds):
    hours, remainder = divmod(seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    return f"{int(hours):02d}:{int(minutes):02d}:{int(seconds):02d}"


async def screenshots(client):
    duration = get_duration("video.mkv")
    n = int(duration/10)
    timestamp = 0
    images = []
    list = []
    for i in range(1,11):
        timestamp +=n
        capture_frame("video.mkv",timestamp , f"ss/{i}.jpg")
        images.append(InputMediaPhoto(f"ss/{i}.jpg",caption=f"Screenshot at {seconds_to_hms(timestamp)}",has_spoilers=True))
        list.append({"image":store_image(f"ss/{i}.jpg"),"seconds":timestamp,"timestamp":seconds_to_hms(timestamp)})
    await client.send_media_group(config.channel_id,images)
    for i in range(1,11):os.remove(f"ss/{i}.jpg")
    return list
