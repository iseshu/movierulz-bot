from pymongo import MongoClient
from config import Config
# Connection to MongoDB
uri = Config().mongodb_uri
client = MongoClient(uri)
db = client['database']
collection = db['data']

class Database:
    def insert(self,data):
        collection.insert_one(data)
    def find(data):
        return collection.find_one(data)
    def find_all(self):
        return collection.find()
    def update(self, data, new_data):
        collection.update_one(data, new_data)
    def delete(self, data):
        collection.delete_one(data)
    def delete_all(self):
        collection.delete_many({})
