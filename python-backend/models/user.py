import bcrypt
import logging
import jwt
import os
import datetime
from models.mongo_model import MongoModel
from pymongo.errors import DuplicateKeyError, CursorNotFound
from pymongo.collection import ReturnDocument
from bson.objectid import ObjectId
from models.user_type import UserType


class User(MongoModel):

    JWT_HASHING_ALGORITHM = 'HS256'
    PWD_ENCODING = 'UTF-8'
    EXPIRED_JWT_HOURS = 24

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
            raise Exception('Required information is missing')

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

    def verify_password(self, user, password):
        try:
            if bcrypt.checkpw(bytes(password, encoding=self.PWD_ENCODING), user['password']):
                encoded_jwt = jwt.encode({
                    'username': user['username'],
                    'id': user['_id'],
                    'role': user['role'],
                    'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=self.EXPIRED_JWT_HOURS)
                }, os.environ['JWT_SECRET'], algorithm=self.JWT_HASHING_ALGORITHM)
                return encoded_jwt
            else:
                return ''
        except jwt.InvalidIssuedAtError as error:
            logging.error(str(error))
            raise Exception(error)

    def verify_user_permission(self, token, user_id=None):
        try:
            if token:
                decoded_jwt = jwt.decode(
                    token, os.environ['JWT_SECRET'], algorithms=self.JWT_HASHING_ALGORITHM)
                if decoded_jwt['role'] == 'admin':
                    return UserType.ADMIN
                elif user_id is not None and decoded_jwt['id'] == user_id:
                    return UserType.AUTHENTICATED_USER

            return UserType.NOT_ALLOWED_USER
        except jwt.ExpiredSignatureError:
            raise Exception('Please relogin, the session has been expired')

    def delete(self, user_id, token):
        if verify_user_permission(token) != UserType.ADMIN:
            raise NotImplementedError('Not permitted to delete user')

        self.database[self.collection].find_one_and_delete(
            {'_id': ObjectId(user_id)})
        return True

    def change_password(self, user_id, token, new_password):
        if verify_user_permission(token, user_id) == UserType.NOT_ALLOWED_USER:
            raise NotImplementedError('Not permitted to execute')

        hashed_password = bcrypt.hashpw(
            bytes(new_password, encoding=self.PWD_ENCODING), bcrypt.gensalt(os.environ['PWD_ROUNDS']))

        self.database[self.collection].find_one_and_update(
            {'_id': ObjectId(user_id)}, {'$set': {'password': hashed_password}}, return_document=ReturnDocument.AFTER)
        return True

    def getAll(self, token):
        if verify_user_permission(token) == UserType.ADMIN:
            users = self.database[self.collection].find(
                {}, {'_id': 0, 'password': 0})
            return users

        return None
