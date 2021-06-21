from models.user import User
from pymongo.errors import DuplicateKeyError
from flask import jsonify


class UserController:

    def register(self, user):
        try:
            user_model = User()
            added_user = user_model.add(user)
            return jsonify(added_user_id=added_user)

        except KeyError as error:
            return jsonify(code=400, message="Missing required information")

        except DuplicateKeyError as error:
            return jsonify(code=400, message='Email %s or Username %s has been invalid' % (user['email'], user['username']))

        except Exception as error:
            return jsonify(code=400, message=str(error))

    def login(self, username, password):
        try:
            user_model = User()
            user = user_model.find_with_username(username)
            token = user_model.verify_password(user, password)

            if token:
                return jsonify(code=200, message="Login successfully", token=token)
            else:
                raise Exception('Username or password is invalid')

        except Exception as error:
            return jsonify(code=400, message=str(error))

    def getAll(self, token):
        try:
            user_model = User()
            users = user_model.getAll(token)
            return jsonify(code=200, users=list(users))
        except Exception as error:
            return jsonify(code=400, message=str(error))

    def delete(self, user_id, token):
        try:
            user_model = User()
            user = user_model.delete(user_id, token)
            return jsonify(code=200, message='The user has been removed successfully')
        except Exception as error:
            return jsonify(code=400, message=str(error))

    def change_password(self, user_id, token, new_password):
        try:
            user_model = User()
            user = user_model.change_password(user_id, token, new_password)
            return jsonify(code=200, message='The password has been changed successfully')
        except Exception as error:
            return jsonify(code=400, message=str(error))

