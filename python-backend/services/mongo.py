import os
from pymongo import MongoClient

MONGO_DB_HOST = os.environ['MONGO_DB_HOST']
MONGO_DB_PORT = os.environ['MONGO_DB_PORT']
MONGO_DB_DATABASE = os.environ['MONGO_DB_DATABASE']
MONGO_DB_USERNAME = os.environ['MONGO_DB_USERNAME']
MONGO_DB_PASSWORD = os.environ['MONGO_DB_PASSWORD']


class Mongo:

    def __init__(self):
        try:
            self.client = MongoClient("mongodb://%s:%s@%s:%s/%s" %
                                      (MONGO_DB_USERNAME, MONGO_DB_PASSWORD,
                                       MONGO_DB_HOST, MONGO_DB_PORT, MONGO_DB_DATABASE))
        except Exception as e:
            print(e.message)

    def get_database(self):
        return self.client[MONGO_DB_DATABASE]
