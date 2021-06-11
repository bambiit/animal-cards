from models.mongo_model import MongoModel
import bcrypt
from pymongo.errors import DuplicateKeyError, CursorNotFound
from pymongo.collection import ReturnDocument
import logging
import jwt
import os


class User(MongoModel):

    JWT_HASHING_ALGORITHM = 'HS256'
    PWD_ENCODING = 'UTF-8'

    def __init__(self):
        super(User, self).__init__()
        self.collection = 'users'
        # if the index already exists, starting from version 3.11, mongo would ignore and not throw an exception
        self.database[self.collection].create_index(
            'email', unique=True)
        self.database[self.collection].create_index(
            'username', unique=True)

    def add(self, user):

        # username, email and password are required
        if not user['username'] or not user['email'] or not user['password']:
            raise Exception('Required information is missing')

        try:
            hashed_password = bcrypt.hashpw(
                bytes(user['password'], encoding=self.PWD_ENCODING), bcrypt.gensalt(os.environ['PWD_ROUNDS']))

            added_user = self.database[self.collection].insert({
                'username': user['username'],
                'password': hashed_password,
                'first_name': user['first_name'],
                'last_name': user['last_name'],
                'email': user['email']
            })

            return added_user
        except DuplicateKeyError as error:
            logging.error(str(error))
            raise DuplicateKeyError(error)
        except Exception as error:
            logging.error(str(error))
            raise Exception(error)

    def find_with_username(self, username):
        try:
            user = self.database[self.collection].find_one({
                'username': username})
            return user
        except CursorNotFound as error:
            logging.error(str(error))
            raise CursorNotFound(error)
        except Exception as error:
            logging.error(str(error))
            raise Exception(error)

    def verify_password(self, username, id, password, db_password):
        try:
            if bcrypt.checkpw(bytes(password, encoding=self.PWD_ENCODING), db_password):
                encoded_jwt = jwt.encode({
                    'username': username,
                    'id': str(id)
                }, os.environ['JWT_SECRET'], algorithm=self.JWT_HASHING_ALGORITHM)
                return encoded_jwt
            else:
                return ''
        except jwt.InvalidIssuedAtError as error:
            logging.error(str(error))
            raise Exception(error)

    def delete(self, username):
        try:
            self.database[self.collection].find_one_and_delete(
                {'username': username})
            return True
        except Exception as error:
            logging.error(str(error))
            raise False

    def update(self, username, update_user):
        try:
            self.database[self.collection].find_one_and_update(
                {'username': username}, {'$set': {'username': update_user['username'], 'password': update_user['password'], 'first_name': update_user['first_name'], 'last_name': update_user['last_name']}}, return_document=ReturnDocument.AFTER)
            return True
        except Exception as error:
            logging.error(str(error))
            raise False

    def getAll(self):
        try:
            users = self.database[self.collection].find(
                {}, {'_id': 0, 'password': 0})
            return users
        except Exception as error:
            logging.error(str(error))
            raise False
