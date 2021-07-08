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
    PWD_ROUNDS = int(os.environ['PWD_ROUNDS'])

    def __init__(self):
        super(User, self).__init__('users')

        # if the index already exists, starting from version 3.11, mongo w∏ould ignore and not throw an exception
        self.database[self.collection].create_index(
            'email', unique=True)
        self.database[self.collection].create_index(
            'username', unique=True)

    def add(self, user):

        # username, email and password are required
        if 'username' not in user or 'email' not in user or 'password' not in user:
            raise KeyError('Required information is missing')

        if 'role' not in user:
            role = 'user'
        else:
            role = user['role']

        try:
            formatted_user = self.format_before_add(user)
            if formatted_user is not None:
                added_user = self.database[self.collection].insert_one(
                    formatted_user)
                return str(added_user.inserted_id)
            return None
        except DuplicateKeyError as error:
            logging.exception('Violation in user uniqueness constraints')
            return None
        except Exception as error:
            logging.exception('Could not register new user')
            return None

    def format_before_add(self, user):
        if 'role' not in user:
            role = 'user'
        else:
            role = user['role']

        try:
            hashed_password = bcrypt.hashpw(
                bytes(user['password'], encoding=self.PWD_ENCODING), bcrypt.gensalt(self.PWD_ROUNDS))
            return {
                'first_name': user['first_name'],
                'last_name': user['last_name'],
                'email': user['email'],
                'username': user['username'],
                'password': hashed_password,
                'role': role
            }
        except Exception as error:
            logging.exception('Could not register new user')
            return None

    def find_by_email(self, email):
        try:
            user = self.database[self.collection].aggregate([
                {'$match': {'email': email}},
                {'$limit': 1},
                {'$project': {'_id': {'$toString': '$_id'},
                              'username': 1,
                              'password': 1,
                              'email': 1,
                              'role': 1}}
            ])
            if user is not None:
                return list(user)[0]

            return None
        except CursorNotFound as error:
            logging.exception(
                'No user is found with email as %s' % email)
            return None
        except Exception as error:
            logging.exception(
                'There has been an error during looking for user with email as %s' % email)
            return None

    def verify_password(self, user, password):
        if bcrypt.checkpw(bytes(password, encoding=self.PWD_ENCODING), user['password']):
            return Jwt.encode_token(user['username'], user['_id'], user['role'])
        return None

    def delete(self, user_id, token):
        if Jwt.verify_user_permission(token) != UserType.ADMIN:
            logging.exception('Not permitted to delete user')
            return False

        self.database[self.collection].find_one_and_delete(
            {'_id': ObjectId(user_id)})
        return True

    def change_password(self, user_id, token, old_password, new_password):
        if Jwt.verify_user_permission(token, user_id) is not UserType.AUTHENTICATED_USER:
            logging.exception(
                'Not permitted to change password for user id %s' % user_id)
            return False

        current_user = self.database[self.collection].find_one(
            {'_id': ObjectId(user_id)}, {'password': 1})

        if current_user is not None:
            if bcrypt.checkpw(bytes(old_password, encoding=self.PWD_ENCODING), current_user['password']):
                hashed_new_password = bcrypt.hashpw(
                    bytes(new_password, encoding=self.PWD_ENCODING),
                    bcrypt.gensalt(self.PWD_ROUNDS)
                )

                self.database[self.collection].find_one_and_update(
                    {'_id': ObjectId(user_id)},
                    {'$set': {'password': hashed_new_password}},
                    return_document=ReturnDocument.AFTER
                )

                return True
            else:
                raise Exception('Old password is not matched')

        return False

    def getAll(self, token):
        if Jwt.verify_user_permission(token) == UserType.ADMIN:
            users = self.database[self.collection].aggregate([
                {'$project': {'_id': {'$toString': '$_id'}, 'first_name': 1,
                              'last_name': 1, 'username': 1, 'email': 1}},
                {'$sort': {'username': 1}}
            ])
            return users

        return None

    def count(self):
        number_of_users = self.database[self.collection].aggregate([
            {'$count': 'num_of_users'}
        ])

        return list(number_of_users)[0]

    def add_many(self, users):
        formatted_users = []
        for user in users:
            formatted_user = self.format_before_add(user)
            if formatted_user is None:
                continue
            formatted_users.append(formatted_user)

        try:
            if formatted_users:
                added_users = self.database[self.collection].insert_many(
                    formatted_users)
                return added_users.inserted_ids
            return None
        except Exception as error:
            logging.exception('Could not bulk inserting for list of users')
            return None
