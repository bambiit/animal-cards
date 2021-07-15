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
