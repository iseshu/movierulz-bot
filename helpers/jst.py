import time
import math
import requests


def convert_bytes(size_bytes):
   if size_bytes == 0:
       return "0B"
   size_name = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
   i = int(math.floor(math.log(size_bytes, 1024)))
   p = math.pow(1024, i)
   s = round(size_bytes / p, 2)
   return "%s %s" % (s, size_name[i])

def convert_seconds_to_eta(seconds):
    if seconds < 60:
        return f"{seconds:.2f} seconds"
    elif seconds < 3600:
        minutes = seconds / 60
        return f"{minutes:.2f} minutes"
    elif seconds < 86400:
        hours = seconds / 3600
        return f"{hours:.2f} hours"
    else:
        days = seconds / 86400
        return f"{days:.2f} days"
    
def generate_progress_bar(percentage, segments=10):
    if not (0 <= percentage <= 100):
        raise ValueError("Percentage must be between 0 and 100")
    
    filled_segments = int(segments * percentage / 100)
    empty_segments = segments - filled_segments
    
    progress_bar = "█" * filled_segments + "▒" * empty_segments
    
    return progress_bar
async def get_torrents(link):
        url = f'https://movierulz.vercel.app/get?url={link}'
        response = requests.get(url)
        info = response.json()

        title = info['title']
        image = info['image']
        description = info['description']
        torrents = []
        for torrent in info['torrent']:
            size = torrent['size']
            if " gb" in size:
                size = float(size.replace(" gb", "")) * 1000
            elif " mb" in size:
                size = float(size.replace(" mb", ""))
            if size < 2000:
                torrents.append(torrent)
        return title,image,description,torrents


