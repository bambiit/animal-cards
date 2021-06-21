import bcrypt
import logging
import os
from helpers.jwt import Jwt
from models.mongo_model import MongoModel
from pymongo.errors import DuplicateKeyError, CursorNotFound
from pymongo.collection import ReturnDocument
from bson.objectid import ObjectId
from models.user_type import UserType


class User(MongoModel):

    PWD_ENCODING = 'UTF-8'

    def __init__(self):
        super(User, self).__init__('users')

        # if the index already exists, starting from version 3.11, mongo w∏ould ignore and not throw an exception
        self.database[self.collection].create_index(
            'email', unique=True)
        self.database[self.collection].create_index(
            'username', unique=True)

    def add(self, user):

        # username, email and password are required
        if not user['username'] or not user['email'] or not user['password']:
            raise KeyError('Required information is missing')

        if not user['role']:
            role = 'user'
        else:
            role = user['role']

        try:
            hashed_password = bcrypt.hashpw(
                bytes(user['password'], encoding=self.PWD_ENCODING), bcrypt.gensalt(os.environ['PWD_ROUNDS']))

            added_user = self.database[self.collection].insert_one({
                'username': user['username'],
                'password': hashed_password,
                'first_name': user['first_name'],
                'last_name': user['last_name'],
                'email': user['email'],
                'role': role
            })

            return added_user
        except DuplicateKeyError as error:
            logging.exception('Violation in user uniqueness constraints')
            return None
        except Exception as error:
            logging.exception('Could not register new user')
            return None

    def find_with_username(self, username):
        try:
            user = self.database[self.collection].find_one({
                'username': username})
            return user
        except CursorNotFound as error:
            logging.exception(
                'No user is found with username as %s' % username)
            return None
        except Exception as error:
            logging.exception(
                'There has been an error during looking for user with username as %s' % username)
            return None

    def verify_password(self, user, password):
        if bcrypt.checkpw(bytes(password, encoding=self.PWD_ENCODING), user['password']):
            return Jwt.encode_token(user['username'], user['id'], user['role'])
        return None

    def delete(self, user_id, token):
        if Jwt.verify_user_permission(token) != UserType.ADMIN:
            logging.exception('Not permitted to delete user')
            return False

        self.database[self.collection].find_one_and_delete(
            {'_id': ObjectId(user_id)})
        return True

    def change_password(self, user_id, token, new_password):
        if Jwt.verify_user_permission(token, user_id) == UserType.NOT_ALLOWED_USER:
            logging.exception(
                'Not permitted to change password for user id %s' % user_id)
            return False

        hashed_password = bcrypt.hashpw(
            bytes(new_password, encoding=self.PWD_ENCODING), bcrypt.gensalt(os.environ['PWD_ROUNDS']))

        self.database[self.collection].find_one_and_update(
            {'_id': ObjectId(user_id)}, {'$set': {'password': hashed_password}}, return_document=ReturnDocument.AFTER)
        return True

    def getAll(self, token):
        if Jwt.verify_user_permission(token) == UserType.ADMIN:
            users = self.database[self.collection].find(
                {}, {'password': 0})
            return users

        return None
