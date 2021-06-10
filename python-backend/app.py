from flask import Flask
from models.user import User
import json
from services.mongo import Mongo

app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route('/users', methods=['GET'])
def get_users():
    print("############Query####################")
    userCollection = User()
    users = userCollection.find()
    return json.dumps(list(users))


if __name__ == '__main__':
    print("#############Starting app##############")
    app.run(host='0.0.0.0', port=8080, debug=True)
