from services.mongo import Mongo
import os


class MongoModel:

    def __init__(self, collection):
        client = Mongo()
        self.database = client.get_database()
        self.collection = collection

    def reset(self):
        if os.environ['SERVICE_ENV'] == 'TESTING':    
            self.database[self.collection].drop()
            return True
        return False
