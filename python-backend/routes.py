from app import app
from flask import request, jsonify
from controllers.user import UserController

####################Users API #######################

def get_token():
    return request.headers.get('Authorization')


@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route('/api/users/', methods=['GET'])
def get_users():
    user_controller = UserController()
    token = get_token()
    return user_controller.getAll(token)


@app.route('/api/users/', methods=['POST'])
def new_user():
    new_user = request.get_json()
    user_controller = UserController()
    return user_controller.register(new_user)


@app.route('/api/users/login/', methods=['POST'])
def login():
    try:
        user_controller = UserController()
        username = request.get_json()['username']
        password = request.get_json()['password']
        return user_controller.login(username, password)
    except KeyError as error:
        return jsonify(code=400, message="Missing required information")


@app.route('/api/users/<user_id>/delete/', methods=['DELETE'])
def delete_user(user_id):
    user_controller = UserController()
    token = get_token()
    return user_controller.delete(user_id, token)


@app.route('/api/users/<user_id>/change_password/', methods=['POST'])
def change_password(user_id):
    try:
        user_controller = UserController()
        token = get_token()
        new_password = request.get_json()['new_password']
        return user_controller.change_password(user_id, token, new_password)

    except KeyError as error:
        return jsonify(code=400, message="Missing new password")


####################Cards API #######################