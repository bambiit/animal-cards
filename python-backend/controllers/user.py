from models.user import User
from pymongo.errors import DuplicateKeyError
from flask import jsonify


class UserController:

    def register(self, user):
        user_model = User()
        added_user_id = user_model.add(user)
        if added_user_id:
            return jsonify(code=201, user_id=added_user_id)

        return jsonify(code=400, message='Could not register new user')

    def login(self, email, password):
        user_model = User()
        user = user_model.find_by_email(email)
        if user is not None:
            token = user_model.verify_password(user, password)

            if token:
                return jsonify(code=200, message="Login successfully", token=token)

        return jsonify(code=400, message='Email or password is invalid')

    def getAll(self, token):
        user_model = User()
        users = user_model.getAll(token)

        if users:
            return jsonify(code=200, users=list(users))

        return jsonify(code=400, message='List of users could not be retrieved')

    def delete(self, user_id, token):
        user_model = User()
        is_deleted = user_model.delete(user_id, token)
        if is_deleted:
            return jsonify(code=204, message='The user has been removed successfully')
        return jsonify(code=400, message='The user has not been removed, the operation is not permitted')

    def change_password(self, user_id, token, old_password, new_password):
        try:
            user_model = User()
            is_password_changed = user_model.change_password(
                user_id, token, old_password, new_password)
            if is_password_changed:
                return jsonify(code=200, message='The password has been changed successfully')
            return jsonify(code=400, message='The password has not been changed, the operation is not permitted')
        except Exception as error:
            return jsonify(code=400, message=str(error))
