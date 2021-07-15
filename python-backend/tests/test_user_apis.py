import pytest
import json
from utils.test_utils import TestUtils
from app import app


@pytest.fixture(autouse=True)
def client():
    with app.test_client() as client:
        TestUtils.reset_database()
        yield client


def test_welcome_page(client):
    rv = client.get('/')
    assert b'Hello World!' in rv.data

######################signup API tests####################


def test_signup_api_successfully(client):
    payload = {
        'username': 'minhbui',
        'password': 'P@ssw0rd',
        'first_name': 'Minh',
        'last_name': 'Bui',
        'email': 'minh.bui@helsinki.fi'
    }

    rv = client.post('/api/users/register', json=payload)
    json_data = json.loads(rv.data)
    assert 'code' in json_data and json_data['code'] == 201
    assert 'user_id' in json_data


def test_signup_api_duplicated_email(client):
    TestUtils.init_users()

    payload = {
        'username': 'minhbui-user-1-duplicated',
        'password': 'P@ssw0rd@User1-Duplicated',
        'first_name': 'Minh',
        'last_name': 'Bui',
        'email': 'minh.bui.user1@helsinki.fi'
    }

    rv = client.post('/api/users/register', json=payload)
    json_data = json.loads(rv.data)
    assert 'code' in json_data and json_data['code'] == 400
    assert 'user_id' not in json_data


def test_signup_api_duplicated_username(client):
    TestUtils.init_users()

    payload = {
        'username': 'minhbui-user-1',
        'password': 'P@ssw0rd@User1-Duplicated',
        'first_name': 'Minh',
        'last_name': 'Bui',
        'email': 'minh.bui.user1.duplicated@helsinki.fi'
    }

    rv = client.post('/api/users/register', json=payload)
    json_data = json.loads(rv.data)
    assert 'code' in json_data and json_data['code'] == 400
    assert 'user_id' not in json_data


######################login API tests####################

def test_login_api_successfully(client):
    TestUtils.init_users()

    payload = {
        'email': 'minh.bui.user1@helsinki.fi',
        'password': 'P@ssw0rd@User1'
    }

    rv = client.post('/api/users/login', json=payload)
    json_data = json.loads(rv.data)
    assert 'code' in json_data and json_data['code'] == 200
    assert 'token' in json_data


def fail_login_action(rv):
    json_data = json.loads(rv.data)
    assert 'code' in json_data and json_data['code'] == 400
    assert 'token' not in json_data


def test_login_api_wrong_email(client):
    TestUtils.init_users()

    payload = {
        'email': 'minh.bui.user1-wrong@helsinki.fi',
        'password': 'P@ssw0rd@User1'
    }

    rv = client.post('/api/users/login', json=payload)
    fail_login_action(rv)


def test_login_api_wrong_password(client):
    TestUtils.init_users()

    payload = {
        'email': 'minh.bui.user1@helsinki.fi',
        'password': 'P@ssw0rd-Wrong'
    }

    rv = client.post('/api/users/login', json=payload)
    fail_login_action(rv)

######################change password API tests####################


def fail_change_password_action(client, rv_change_password, email, new_password):
    rv_change_password_json = json.loads(rv_change_password.data)
    assert rv_change_password_json['code'] == 400

    login_payload = {
        'email': email,
        'password': new_password
    }

    rv_login = client.post('/api/users/login', json=login_payload)
    json_data = json.loads(rv_login.data)
    assert 'code' in json_data and json_data['code'] == 400
    assert 'token' not in json_data


def test_change_password_successfully(client):
    TestUtils.init_users()
    user_id, token = TestUtils.retrieve_token(
        'minh.bui.user1@helsinki.fi', 'P@ssw0rd@User1')

    change_password_payload = {
        'old_password': 'P@ssw0rd@User1',
        'new_password': 'P@ssw0rd@User1-New'
    }

    rv_change_password = client.post('/api/users/%s/change_password' % user_id,
                                     json=change_password_payload,
                                     headers={'Authorization': 'Bearer %s' % token})

    rv_change_password_json = json.loads(rv_change_password.data)
    assert rv_change_password_json['code'] == 200

    login_payload = {
        'email': 'minh.bui.user1@helsinki.fi',
        'password': 'P@ssw0rd@User1-New'
    }

    rv_login = client.post('/api/users/login', json=login_payload)
    json_data = rv_login.data
    assert b'token' in json_data


def test_change_password_without_authorization(client):
    TestUtils.init_users()
    user_id = TestUtils.retrieve_user_id(
        'minh.bui.user1@helsinki.fi')

    change_password_payload = {
        'old_password': 'P@ssw0rd@User1',
        'new_password': 'P@ssw0rd@User1-New'
    }

    rv_change_password = client.post('/api/users/%s/change_password' % user_id,
                                     json=change_password_payload)
    fail_change_password_action(
        client, rv_change_password, 'minh.bui.user1@helsinki.fi', 'P@ssw0rd@User1-New')


def test_change_password_without_payload(client):
    TestUtils.init_users()
    user_id, token = TestUtils.retrieve_token(
        'minh.bui.user1@helsinki.fi', 'P@ssw0rd@User1')

    rv_change_password = client.post('/api/users/%s/change_password' % user_id,
                                     headers={'Authorization': 'Bearer %s' % token})

    fail_change_password_action(
        client, rv_change_password, 'minh.bui.user1@helsinki.fi', 'P@ssw0rd@User1-New')


def test_change_password_wrong_old_password(client):
    TestUtils.init_users()
    user_id, token = TestUtils.retrieve_token(
        'minh.bui.user1@helsinki.fi', 'P@ssw0rd@User1')

    change_password_payload = {
        'old_password': 'P@ssw0rd@User1-Wrong',
        'new_password': 'P@ssw0rd@User1-New'
    }

    rv_change_password = client.post('/api/users/%s/change_password' % user_id,
                                     json=change_password_payload,
                                     headers={'Authorization': 'Bearer %s' % token})

    fail_change_password_action(
        client, rv_change_password, 'minh.bui.user1@helsinki.fi', 'P@ssw0rd@User1-New')


def test_change_password_unauthenticated_user_id(client):
    TestUtils.init_users()

    # get target user id
    user_id = TestUtils.retrieve_user_id(
        'minh.bui.user1@helsinki.fi')

    # logged in with other user
    logged_in_user_id, token = TestUtils.retrieve_token(
        'minh.bui.user2@helsinki.fi', 'P@ssw0rd@User2')

    change_password_payload = {
        'old_password': 'P@ssw0rd@User1',
        'new_password': 'P@ssw0rd@User1-New'
    }

    # change password of user 1 with token of logged in user 2
    rv_change_password = client.post('/api/users/%s/change_password' % user_id,
                                     json=change_password_payload,
                                     headers={'Authorization': 'Bearer %s' % token})

    fail_change_password_action(
        client, rv_change_password, 'minh.bui.user1@helsinki.fi', 'P@ssw0rd@User1-New')


def test_change_password_with_admin_user(client):
    TestUtils.init_users()

    # get target user id
    user_id = TestUtils.retrieve_user_id(
        'minh.bui.user1@helsinki.fi')

    # logged in with other user
    logged_in_user_id, token = TestUtils.retrieve_token(
        'minh.bui.admin@helsinki.fi', 'P@ssw0rd@Admin')

    change_password_payload = {
        'old_password': 'P@ssw0rd@User1',
        'new_password': 'P@ssw0rd@User1-New'
    }

    # change password of user 1 with token of logged in user 2
    rv_change_password = client.post('/api/users/%s/change_password' % user_id,
                                     json=change_password_payload,
                                     headers={'Authorization': 'Bearer %s' % token})

    fail_change_password_action(
        client, rv_change_password, 'minh.bui.user1@helsinki.fi', 'P@ssw0rd@User1-New')


######################get all user API tests####################
def test_get_all_with_admin_user_successfully(client):
    TestUtils.init_users()

    user_id, token = TestUtils.retrieve_token(
        'minh.bui.admin@helsinki.fi', 'P@ssw0rd@Admin')

    # change password of user 1 with token of logged in user 2
    rv = client.get(
        '/api/users', headers={'Authorization': 'Bearer %s' % token})

    rv_json_data = json.loads(rv.data)
    assert 'code' in rv_json_data and rv_json_data['code'] == 200
    assert 'users' in rv_json_data and len(rv_json_data['users']) == 3

    for user in rv_json_data['users']:
        assert 'password' not in user


def test_get_all_without_normal_user(client):
    TestUtils.init_users()

    user_id, token = TestUtils.retrieve_token(
        'minh.bui.user1@helsinki.fi', 'P@ssw0rd@User1')

    # change password of user 1 with token of logged in user 2
    rv = client.get(
        '/api/users', headers={'Authorization': 'Bearer %s' % token})

    rv_json_data = json.loads(rv.data)
    assert 'code' in rv_json_data and rv_json_data['code'] == 400
    assert 'users' not in rv_json_data


######################remove user API tests####################
def test_remove_user_with_admin_user_successfully(client):
    TestUtils.init_users()

    admin_user_id, token = TestUtils.retrieve_token(
        'minh.bui.admin@helsinki.fi', 'P@ssw0rd@Admin')

    user_id = TestUtils.retrieve_user_id(
        'minh.bui.user1@helsinki.fi')

    rv = client.post('/api/users/%s/delete' % user_id,
                     headers={'Authorization': 'Bearer %s' % token})

    rv_json_data = json.loads(rv.data)
    assert 'code' in rv_json_data and rv_json_data['code'] == 204

    number_of_users = TestUtils.get_numbers_of_users()
    assert number_of_users == 2


def test_remove_user_with_normal_user(client):
    TestUtils.init_users()

    logged_in_user_id, token = TestUtils.retrieve_token(
        'minh.bui.user1@helsinki.fi', 'P@ssw0rd@User1')

    user_id = TestUtils.retrieve_user_id(
        'minh.bui.user2@helsinki.fi')

    rv = client.post('/api/users/%s/delete' % user_id,
                     headers={'Authorization': 'Bearer %s' % token})

    rv_json_data = json.loads(rv.data)
    assert 'code' in rv_json_data and rv_json_data['code'] == 400

    number_of_users = TestUtils.get_numbers_of_users()
    assert number_of_users == 3
