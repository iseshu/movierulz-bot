from seedrcc import Login,Seedr
from config import Config
config = Config()
seedr = Login(config.seedr_username, config.seedr_password)
seedr.authorize()
account = Seedr(token=seedr.token)
def deleteAll()->None:
    response = account.listContents()
    if response['files'] != []:
        for file in response['files']:
            account.deleteFile(file['id'])
    if response['folders'] != []:
        for folder in response['folders']:
            account.deleteFolder(folder['id'])
    if response['torrents'] != []:
        for file in response['torrents']:
            account.deleteTorrent(file['id'])

def select_File(response:dict):
    if response['files']:
        for file in response['files']:
            if '.mp4' in file['name'] or '.mkv' in file['name'] and file['size'] < 2147483648 and float(file['video_progress'])==100:
                return file['name'],account.fetchFile(file['folder_file_id'])['url']
    elif response['folders']:
        response = account.listContents(folderId=response['folders'][0]['id'])
        return select_File(response)
def upload_torrent(url:str)->None:
    response = account.addTorrent(url)
def respose()->dict:
    response = account.listContents()
    return response

