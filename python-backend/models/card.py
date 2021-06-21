from models.mongo_model import MongoModel
from bson.objectid import ObjectId
from models.user_type import UserType
from helpers.jwt import Jwt

import logging


class Card(MongoModel):

    def __init__(self):
        super(Card, self).__init__('cards')
        self.database[self.collection].create_index('title', unique=True)

    def add(self, card, token):
        try:
            author = Jwt.get_user_id(token)
            if card['author']:
                author = {
                    '$ref': 'users',
                    '$id': ObjectId(author)
                }

            added_card = self.database[self.collection].insert_one({
                'title': card['title'],
                'author': author,
                'content': card['content'],
                'image': card['image'],
                'price': card['price'],
                'quantity': card['quantity']
            })
            return added_card
        except KeyError as error:
            logging.exception('No valid author has been found')
            return None
        except Exception as error:
            logging.exception('Could not add new card')
            return None

    def get_all(self):
        cards = self.database[self.collection].find({})
        return cards

    def get_cards_by_author(self, author_id):
        if not author_id:
            return get_all(self)

        cards = self.database[self.collection].find(
            {'author.$id': ObjectId(author_id)})
        return cards

    def remove_card(self, card_id, token):
        if not card_id:
            return False

        card = self.database[self.collection].find_one({'_id': ObjectId(card_id)})

        if Jwt.verify_user_permission(token, card['author.$id']) == UserType.NOT_ALLOWED_USER:
            return False

        self.database[self.collection].find_one_and_delete(
            {'_id': ObjectId(card_id)})
        return True
