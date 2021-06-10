from services.mongo import Mongo


class MongoModel:

    def __init__(self):
        client = Mongo()
        self.database = client.get_database()
        self.collection = None

    def find(self, query={}, columns={}):
        return self.database[self.collection].find({})
