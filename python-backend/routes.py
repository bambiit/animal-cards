from app import app
from flask import request, jsonify
from controllers.user import UserController
from controllers.card import CardController

app.url_map.strict_slashes = False

####################Users API #######################


def get_token():
    authorization = request.headers.get('Authorization')
    if authorization:
        data = request.headers.get('Authorization')
        return str.replace(str(data), 'Bearer', '').strip()
    return None


@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route('/api/users/', methods=['GET'])
def get_users():
    user_controller = UserController()
    token = get_token()
    return user_controller.getAll(token)


@app.route('/api/users/register/', methods=['POST'])
def new_user():
    new_user = request.get_json()
    user_controller = UserController()
    return user_controller.register(new_user)


@app.route('/api/users/login/', methods=['POST'])
def login():
    if request.get_json() and 'email' in request.get_json() and 'password' in request.get_json():
        user_controller = UserController()
        email = request.get_json()['email']
        password = request.get_json()['password']
        return user_controller.login(email, password)

    return jsonify(code=400, message="Missing required information")


@app.route('/api/users/<user_id>/delete/', methods=['DELETE'])
def delete_user(user_id):
    user_controller = UserController()
    token = get_token()
    return user_controller.delete(user_id, token)


@app.route('/api/users/<user_id>/change_password/', methods=['PUT'])
def change_password(user_id):
    if request.get_json() and 'new_password' in request.get_json() and 'old_password' in request.get_json():
        user_controller = UserController()
        token = get_token()
        new_password = request.get_json()['new_password']
        old_password = request.get_json()['old_password']
        return user_controller.change_password(user_id, token, old_password, new_password)

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


@app.route('/api/cards/add/', methods=['POST'])
def add_card():
    token = get_token()
    new_card = request.get_json()
    card_controller = CardController()
    return card_controller.add_card(new_card, token)


@app.route('/api/cards/<card_id>/update/', methods=['PUT'])
def update_card(card_id):
    token = get_token()
    update_card = request.get_json()
    card_controller = CardController()
    return card_controller.update_card(card_id, update_card, token)
