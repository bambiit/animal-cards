import jwt
import os
import datetime
import logging
from models.user_type import UserType


class Jwt():

    JWT_HASHING_ALGORITHM = 'HS256'
    EXPIRED_JWT_HOURS = 24
    JWT_SECRET = os.environ['JWT_SECRET']

    @classmethod
    def verify_user_permission(cls, token, user_id=None):
        if token:
            user = Jwt.decode_token(token)
            if user is not None:
                if user['role'] == 'admin':
                    return UserType.ADMIN
                elif user_id is not None and user['_id'] == user_id:
                    return UserType.AUTHENTICATED_USER

        return UserType.NOT_ALLOWED_USER

    @classmethod
    def get_user_id(cls, token):
        if token:
            user = Jwt.decode_token(token)
            if user is not None:
                return user['_id']
        return None

    @classmethod
    def decode_token(cls, token):
        try:
            return jwt.decode(
                token, Jwt.JWT_SECRET, algorithms=Jwt.JWT_HASHING_ALGORITHM)
        except Exception as error:
            logging.exception(error)
            return None

    @classmethod
    def encode_token(cls, username, id, role):
        try:
            encoded_jwt = jwt.encode({
                'username': username,
                '_id': id,
                'role': role,
                'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=Jwt.EXPIRED_JWT_HOURS)
            }, Jwt.JWT_SECRET, algorithm=Jwt.JWT_HASHING_ALGORITHM)
            return encoded_jwt
        except jwt.InvalidIssuedAtError as error:
            logging.exception('Could not encode to return token to user')
            return None
