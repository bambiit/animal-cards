import random
from models.user import User
from models.card import Card


class TestUtils():

    INITIAL_USERS = [
        {
            'username': 'minhbui-admin',
            'password': 'P@ssw0rd@Admin',
            'first_name': 'Minh',
            'last_name': 'Bui',
            'email': 'minh.bui.admin@helsinki.fi',
            'role': 'admin'
        },
        {
            'username': 'minhbui-user-1',
            'password': 'P@ssw0rd@User1',
            'first_name': 'Minh',
            'last_name': 'Bui',
            'email': 'minh.bui.user1@helsinki.fi'
        },
        {
            'username': 'minhbui-user-2',
            'password': 'P@ssw0rd@User2',
            'first_name': 'Minh',
            'last_name': 'Bui',
            'email': 'minh.bui.user2@helsinki.fi'
        }
    ]

    INITIAL_CARDS = [
        {
            'title': 'Tiger',
            'content': 'This is a content for tiger card',
            'image': 'https://wwf.fi/tiger',
            'price': '99.99',
            'unit': 'EUR',
            'quantity': '99'
        },
        {
            'title': 'Lion',
            'content': 'This is a content for lion card',
            'image': 'https://wwf.fi/lion',
            'price': '199.99',
            'unit': 'EUR',
            'quantity': '10'
        },
        {
            'title': 'Wolf',
            'content': 'This is a content for wolf card',
            'image': 'https://wwf.fi/wolf',
            'price': '200.99',
            'unit': 'EUR',
            'quantity': '20'
        }
    ]

    @classmethod
    def reset_database(cls):
        # reset cards
        card_model = Card()
        card_model.reset()

        # reset users
        user_model = User()
        user_model.reset()

    @classmethod
    def init_users(cls):
        user_model = User()
        return user_model.add_many(TestUtils.INITIAL_USERS)

    @classmethod
    def retrieve_token(cls, email, password):
        user_model = User()
        user = user_model.find_by_email(email)
        return user['_id'], user_model.verify_password(user, password)

    @classmethod
    def retrieve_user_id(cls, email):
        user_model = User()
        user = user_model.find_by_email(email)
        return user['_id']

    @classmethod
    def get_numbers_of_users(cls):
        user_model = User()
        return user_model.count()

    @classmethod
    def init_cards_with_random_authors(cls, user_ids=[]):
        if user_ids:
            inserted_ids = user_ids
        else:
            inserted_ids = TestUtils.init_users()

        users_len = len(user_ids)
        cards = []

        for init_card in TestUtils.INITIAL_CARDS:
            card = init_card
            card['author'] = inserted_ids[random.randint(0, users_len)]
            cards.append(card)

        card_model = Card()
        return card_model.add_many(cards)

    @classmethod
    def init_cards_with_specific_author(cls, author_id):
        if not author_id:
            return

        cards = []
        for init_card in TestUtils.INITIAL_CARDS:
            card = init_card
            card['author'] = author_id
            cards.append(card)

        card_model = Card()
        return card_model.add_many(cards)

    @classmethod
    def get_numbers_of_cards(cls):
        card_model = Card()
        return card_model.count()
