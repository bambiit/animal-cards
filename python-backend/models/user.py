from models.mongo_model import MongoModel


class User(MongoModel):
    def __init__(self):
        super(User, self).__init__()
        self.collection = 'users'
