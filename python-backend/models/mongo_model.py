from services.mongo import Mongo


class MongoModel:

    def __init__(self, collection):
        client = Mongo()
        database = client.get_database()
        self.collection = collection

        # Aggregate for _id returns as string
        self.database[self.collection].aggregate([
            {'project': {'_id': {'$toString': '$_id'}}}
        ])
