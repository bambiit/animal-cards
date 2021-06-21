import jwt
import os
import datetime
import logging
from models.user_type import UserType


class Jwt():

    JWT_HASHING_ALGORITHM = 'HS256'
    EXPIRED_JWT_HOURS = 24

    @classmethod
    def verify_user_permission(cls, token, user_id=None):
        if token:
            decoded_jwt = decoded_jwt(token)
            if decoded_jwt['role'] == 'admin':
                return UserType.ADMIN
            elif user_id is not None and decoded_jwt['id'] == user_id:
                return UserType.AUTHENTICATED_USER

        return UserType.NOT_ALLOWED_USER

    @classmethod
    def get_user_id(cls, token):
      if token:
        decoded_jwt = decoded_jwt(token)
        return decoded_jwt['id']
      return None

    @classmethod
    def decode_token(cls, token):
      return jwt.decode(
                token, os.environ['JWT_SECRET'], algorithms=Jwt.JWT_HASHING_ALGORITHM)

    @classmethod
    def encode_token(cls, username, id, role):
        try:
            encoded_jwt = jwt.encode({
                'username': username,
                'id': id,
                'role': role,
                'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=Jwt.EXPIRED_JWT_HOURS)
            }, os.environ['JWT_SECRET'], algorithm=Jwt.JWT_HASHING_ALGORITHM)
            return encoded_jwt
        except jwt.InvalidIssuedAtError as error:
            logging.exception('Could not encode to return token to user')
            return None
