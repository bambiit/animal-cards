from models.mongo_model import MongoModel
from bson.objectid import ObjectId
from models.user_type import UserType
from helpers.jwt import Jwt
from pymongo.collection import ReturnDocument

import logging


class Card(MongoModel):

    def __init__(self):
        super(Card, self).__init__('cards')
        self.database[self.collection].create_index('title', unique=True)

    def add(self, card, token):
        try:
            author_id = Jwt.get_user_id(token)

            added_card = self.database[self.collection].insert_one(
                self.format_before_add(card, author_id))

            return str(added_card.inserted_id)

        except Exception as error:
            logging.exception(error)
            return None

    def format_before_add(self, card, author_id):
        return {
            'title': card['title'],
            'author': ObjectId(author_id),
            'content': card['content'],
            'image': card['image'],
            'price': card['price'],
            'quantity': card['quantity']
        }

    def get_all(self):
        cards = self.database[self.collection].aggregate([
            {'$project': {'_id': {'$toString': '$_id', 'author': 0}}},
            {'$lookup':
                {
                    'from': 'users',
                    'localField': 'author',
                    'foreignField': '_id',
                    'pipeline': [{
                        '$project': {'password': 0, 'role': 0, 'email': 0}
                    }],
                    'as': 'author_info'
                }
             }
        ])
        return cards

    def get_cards_by_author(self, author_id):
        if not author_id:
            return get_all(self)

        cards = self.database[self.collection].aggregate([
            {'$match': {'author': ObjectId(author_id)}},
            {'$project': {'_id': {'$toString': '$_id', 'author': 0}}}
        ])
        return cards

    def remove_card(self, card_id, token):
        if not card_id:
            return False

        card = self.database[self.collection].find_one(
            {'_id': ObjectId(card_id)})

        if Jwt.verify_user_permission(token, card['author.$id']) == UserType.NOT_ALLOWED_USER:
            return False

        self.database[self.collection].find_one_and_delete(
            {'_id': ObjectId(card_id)})
        return True

    def update_card(self, card_id, card, token):
        if Jwt.verify_user_permission(token) == UserType.NOT_ALLOWED_USER:
            logging.exception(
                'Not permitted to update card with card id %s' % card['_id'])
            return False

        self.database[self.collection].find_one_and_update(
            {'_id': ObjectId(card_id)},
            {'$set': {'title': card['title'],
                      'content': card['content'],
                      'image': card['image'],
                      'price': card['price'],
                      'quantity': card['quantity']}}, return_document=ReturnDocument.AFTER)
        return True

    def add_many(self, cards):
        try:
            formatted_cards = []
            for card in cards:
                formatted_cards.append(
                    self.format_before_add(card, card['author']))
            if formatted_cards:
                added_cards = self.database[self.collection].insert_many(
                    formatted_cards)
                return added_cards.inserted_ids
        except Exception as error:
            logging.exception(error)
            return None
