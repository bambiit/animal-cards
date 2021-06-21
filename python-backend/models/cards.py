from models.mongo_model import MongoModel
from bson.objectid import ObjectId

class Cards(MongoModel):

    def __init__(self):
        super(Cards, self).__init__('cards')
        self.database[self.collection].create_index('title', unique=True)

    def add(self, card):

        author = None
        if card['author']:
            author = {
                '$ref': 'users',
                '$id': ObjectId(card['author'])
            }

        self.database[self.collection].insert_one({
            'title': card['title'],
            'author': author,
            'content': card['content'],
            'image': card['image'],
            'price': card['price'],
            'quantity': card['quantity']
        })
        # title, tags, author, content, image, price, quantity
