import pytest
import json
from app import app
from utils.test_utils import TestUtils


@pytest.fixture(autouse=True)
def client():
    with app.test_client() as client:
        TestUtils.reset_database()
        yield client

######################get all card API tests####################


def test_get_all_cards_successfully(client):
    TestUtils.init_cards_with_random_authors()

    rv = client.get('/api/cards/')
    rv_data_json = json.loads(rv.data)
    assert 'code' in rv_data_json and rv_data_json['code'] == 200
    assert 'cards' in rv_data_json and len(rv_data_json['cards']) == 3

    for card in rv_data_json['cards']:
        assert 'author_info' in card
        assert 'password' not in card['author_info']
        assert 'email' not in card['author_info']
        assert 'role' not in card['author_info']

######################get cards by author API tests####################


def test_get_all_cards_by_author_successfully(client):
    user_ids = TestUtils.init_users()
    assert len(user_ids) >= 3

    author_id = user_ids[0]
    TestUtils.init_cards_with_specific_author(author_id)

    rv = client.get('/api/cards/%s/' % author_id)
    rv_data_json = json.loads(rv.data)
    assert 'code' in rv_data_json and rv_data_json['code'] == 200
    assert 'cards' in rv_data_json and len(rv_data_json['cards']) == 3


def test_get_all_cards_by_author_no_card_found(client):
    user_ids = TestUtils.init_users()
    assert len(user_ids) >= 3

    author_id = user_ids[0]
    TestUtils.init_cards_with_specific_author(author_id)

    rv = client.get('/api/cards/%s/' % user_ids[1])
    rv_data_json = json.loads(rv.data)
    assert 'code' in rv_data_json and rv_data_json['code'] == 200
    assert 'cards' in rv_data_json and len(rv_data_json['cards']) == 0


def test_get_all_cards_by_author_not_valid_author_id(client):
    user_ids = TestUtils.init_users()
    assert len(user_ids) >= 3

    author_id = user_ids[0]
    TestUtils.init_cards_with_specific_author(author_id)

    rv = client.get('/api/cards/%s/' % 'not_valid_author_id')
    rv_data_json = json.loads(rv.data)
    assert 'code' in rv_data_json and rv_data_json['code'] == 400
    assert 'cards' not in rv_data_json

######################delete card API tests####################


def test_delete_card_by_admin_successfully(client):
    user_ids = TestUtils.init_users()
    assert len(user_ids) >= 3

    # user 1 in test data is normal user
    author_id = TestUtils.retrieve_user_id('minh.bui.user1@helsinki.fi')
    inserted_card_ids = TestUtils.init_cards_with_specific_author(author_id)
    assert TestUtils.get_numbers_of_cards() == 3

    # logged in with admin user
    logged_in_user_id, token = TestUtils.retrieve_token(
        'minh.bui.admin@helsinki.fi', 'P@ssw0rd@Admin')

    rv = client.delete('/api/cards/%s/delete/' % inserted_card_ids[0],
                       headers={'Authorization': 'Bearer %s' % token})

    rv_data_json = json.loads(rv.data)
    assert 'code' in rv_data_json and rv_data_json['code'] == 204
    assert TestUtils.get_numbers_of_cards() == 2


def test_delete_card_by_author_successfully(client):
    user_ids = TestUtils.init_users()
    assert len(user_ids) >= 3

    # user 1 in test data is normal user
    author_id = TestUtils.retrieve_user_id('minh.bui.user1@helsinki.fi')
    inserted_card_ids = TestUtils.init_cards_with_specific_author(author_id)
    assert TestUtils.get_numbers_of_cards() == 3

    # logged in with author user
    logged_in_user_id, token = TestUtils.retrieve_token(
        'minh.bui.user1@helsinki.fi', 'P@ssw0rd@User1')

    rv = client.delete('/api/cards/%s/delete/' % inserted_card_ids[0],
                       headers={'Authorization': 'Bearer %s' % token})

    rv_data_json = json.loads(rv.data)
    assert 'code' in rv_data_json and rv_data_json['code'] == 204
    assert TestUtils.get_numbers_of_cards() == 2


def test_delete_card_by_other_author(client):
    user_ids = TestUtils.init_users()
    assert len(user_ids) >= 3

    # user 1 in test data is normal user
    author_id = TestUtils.retrieve_user_id('minh.bui.user1@helsinki.fi')
    inserted_card_ids = TestUtils.init_cards_with_specific_author(author_id)
    assert TestUtils.get_numbers_of_cards() == 3

    # logged in with author user
    logged_in_user_id, token = TestUtils.retrieve_token(
        'minh.bui.user2@helsinki.fi', 'P@ssw0rd@User2')

    rv = client.delete('/api/cards/%s/delete/' % inserted_card_ids[0],
                       headers={'Authorization': 'Bearer %s' % token})

    rv_data_json = json.loads(rv.data)
    assert 'code' in rv_data_json and rv_data_json['code'] == 400
    assert TestUtils.get_numbers_of_cards() == 3

######################add new card API tests####################


def test_add_new_card_successfully(client):

    TestUtils.init_users()

    # user 1 log in with normal user
    logged_in_user_id, token = TestUtils.retrieve_token(
        'minh.bui.user1@helsinki.fi', 'P@ssw0rd@User1')

    payload = {
        'title': 'Snow Leopard',
        'content': 'This is a content for snow leopard card',
        'image': 'https://wwf.fi/snow-leopard',
        'price': '199.99',
        'unit': 'EUR',
        'quantity': '99'
    }

    rv = client.put('/api/cards/add/', json=payload,
                    headers={'Authorization': 'Bearer %s' % token})
    rv_data_json = json.loads(rv.data)
    assert 'code' in rv_data_json and rv_data_json['code'] == 201
    assert 'new_card_id' in rv_data_json
    assert TestUtils.get_numbers_of_cards() == 1


def test_add_new_card_without_login(client):

    payload = {
        'title': 'Snow Leopard',
        'content': 'This is a content for snow leopard card',
        'image': 'https://wwf.fi/snow-leopard',
        'price': '199.99',
        'unit': 'EUR',
        'quantity': '99'
    }

    rv = client.put('/api/cards/add/', json=payload)
    rv_data_json = json.loads(rv.data)
    assert 'code' in rv_data_json and rv_data_json['code'] == 400
    assert 'new_card_id' not in rv_data_json
    assert TestUtils.get_numbers_of_cards() == 0


def test_add_new_card_missing_required_information(client):

    TestUtils.init_users()

    # user 1 log in with normal user
    logged_in_user_id, token = TestUtils.retrieve_token(
        'minh.bui.user1@helsinki.fi', 'P@ssw0rd@User1')

    payload = {
        'content': 'This is a content for snow leopard card',
        'image': 'https://wwf.fi/snow-leopard',
        'price': '199.99',
        'unit': 'EUR',
        'quantity': '99'
    }

    rv = client.put('/api/cards/add/', json=payload,
                    headers={'Authorization': 'Bearer %s' % token})
    rv_data_json = json.loads(rv.data)
    assert 'code' in rv_data_json and rv_data_json['code'] == 400
    assert 'new_card_id' not in rv_data_json
    assert TestUtils.get_numbers_of_cards() == 0

######################update card API tests####################


def test_update_card_by_author_successfully(client):
    user_ids = TestUtils.init_users()
    assert len(user_ids) >= 3

    # user 1 in test data is normal user
    author_id = TestUtils.retrieve_user_id('minh.bui.user1@helsinki.fi')
    inserted_card_ids = TestUtils.init_cards_with_specific_author(author_id)
    assert TestUtils.get_numbers_of_cards() == 3

    # logged in with author user
    logged_in_user_id, token = TestUtils.retrieve_token(
        'minh.bui.user1@helsinki.fi', 'P@ssw0rd@User1')

    payload = {
        'content': 'This is an updated content',
        'image': 'https://wwf.fi/update-url'
    }

    rv = client.post('/api/cards/%s/update/' % inserted_card_ids[0],
                     json=payload,
                     headers={'Authorization': 'Bearer %s' % token})

    rv_data_json = json.loads(rv.data)
    assert 'code' in rv_data_json and rv_data_json['code'] == 200
    assert 'updated_card' in rv_data_json
    assert 'content' in rv_data_json['updated_card'] and rv_data_json[
        'updated_card']['content'] == 'This is an updated content'
    assert 'image' in rv_data_json['updated_card'] and rv_data_json['updated_card']['image'] == 'https://wwf.fi/update-url'


def test_update_card_by_admin(client):
    user_ids = TestUtils.init_users()
    assert len(user_ids) >= 3

    # user 1 in test data is normal user
    author_id = TestUtils.retrieve_user_id('minh.bui.user1@helsinki.fi')
    inserted_card_ids = TestUtils.init_cards_with_specific_author(author_id)
    assert TestUtils.get_numbers_of_cards() == 3

    # logged in with admin user
    logged_in_user_id, token = TestUtils.retrieve_token(
        'minh.bui.admin@helsinki.fi', 'P@ssw0rd@Admin')

    payload = {
        'content': 'This is an updated content',
        'image': 'https://wwf.fi/update-url'
    }

    rv = client.post('/api/cards/%s/update/' % inserted_card_ids[0],
                     json=payload,
                     headers={'Authorization': 'Bearer %s' % token})

    rv_data_json = json.loads(rv.data)
    assert 'code' in rv_data_json and rv_data_json['code'] == 400
    assert 'updated_card' not in rv_data_json


def test_update_card_by_other_user(client):
    user_ids = TestUtils.init_users()
    assert len(user_ids) >= 3

    # user 1 in test data is normal user
    author_id = TestUtils.retrieve_user_id('minh.bui.user1@helsinki.fi')
    inserted_card_ids = TestUtils.init_cards_with_specific_author(author_id)
    assert TestUtils.get_numbers_of_cards() == 3

    # logged in with admin user
    logged_in_user_id, token = TestUtils.retrieve_token(
        'minh.bui.user2@helsinki.fi', 'P@ssw0rd@User2')

    payload = {
        'content': 'This is an updated content',
        'image': 'https://wwf.fi/update-url'
    }

    rv = client.post('/api/cards/%s/update/' % inserted_card_ids[0],
                     json=payload,
                     headers={'Authorization': 'Bearer %s' % token})

    rv_data_json = json.loads(rv.data)
    assert 'code' in rv_data_json and rv_data_json['code'] == 400
    assert 'updated_card' not in rv_data_json
