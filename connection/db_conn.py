from pymongo import MongoClient

from config import Settings

global_settings = Settings()


class ConnectionMongo:
    def __init__(self):

        self.client = MongoClient(global_settings.MONGODB_URL)

        self.db = self.client.crm

        self.customer = self.db.customer
