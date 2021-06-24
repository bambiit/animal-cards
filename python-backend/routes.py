from app import app
from flask import request, jsonify
from controllers.user import UserController
from controllers.card import CardController

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


@app.route('/api/users/register', methods=['PUT'])
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
@app.route('/api/cards/', methods=['GET'])
def get_cards():
    card_controller = CardController()
    return card_controller.get_all()


@app.route('/api/cards/<author_id>/', methods=['GET'])
def get_cards_by_author(author_id):
    card_controller = CardController()
    cards = card_controller.get_all_filtered_by_author(author_id)
    return cards


@app.route('/api/cards/<card_id>/delete/', methods=['DELETE'])
def delete_card(card_id):
    token = get_token()
    card_controller = CardController()
    return card_controller.remove_card(card_id, token)


@app.route('/api/cards/add/', methods=['PUT'])
def add_card():
    token = get_token()
    new_card = request.get_json()
    card_controller = CardController()
    return card_controller.add_card(new_card, token)


@app.route('/api/cards/<card_id>/update/', methods=['POST'])
def update_card(card_id):
    token = get_token()
    update_card = request.get_json()
    card_controller = CardController()
    return card_controller.update_card(card_id, update_card, token)
