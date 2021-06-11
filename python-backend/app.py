from flask import Flask, request, jsonify
from controllers.user import UserController
from helpers.JSONEncoder import JSONEncoder
import json
import os

app = Flask(__name__)
app.json_encoder = JSONEncoder


@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route('/api/users', methods=['GET'])
def get_users():
    user_controller = UserController()
    return user_controller.getAll()


@app.route('/api/users', methods=['POST'])
def new_user():
    new_user = request.get_json()
    user_controller = UserController()
    return user_controller.add_user(new_user)


@app.route('/api/users/login', methods=['POST'])
def login():
    try:
        user_controller = UserController()
        username = request.get_json()['username']
        password = request.get_json()['password']
        return user_controller.login(username, password)
    except KeyError as error:
        return jsonify(code=400, message="Missing required information")


if __name__ == '__main__':
    print("#############Starting app##############")
    app.run(host=os.environ['ANIMAL_CARDS_HOST'],
            port=os.environ['ANIMAL_CARDS_PORT'], debug=os.environ['DEBUG_MODE'])
