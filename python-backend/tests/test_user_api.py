import pytest
from flask import Flask
from app import app


@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


def test_welcome_page(client):
    rv = client.get('/')
    assert b'Hello World!' in rv.data
