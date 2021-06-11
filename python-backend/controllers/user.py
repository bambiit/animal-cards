from models.user import User
from pymongo.errors import DuplicateKeyError
from flask import jsonify


class UserController:
    def add_user(self, user):
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
            token = user_model.verify_password(
                username, user['_id'], password, user['password'])

            if token:
                return jsonify(code=200, message="Login successfully", token=token)
            else:
                raise InvalidUserError('The password is invalid')

        except Exception as error:
            return jsonify(code=400, message="Username or password is invalid")

    def getAll(self):
        user_model = User()
        users = user_model.getAll()
        return jsonify(code=200, users=list(users))
