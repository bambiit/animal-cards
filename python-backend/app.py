import os
from flask import Flask
from helpers.JSONEncoder import JSONEncoder

app = Flask(__name__)
app.json_encoder = JSONEncoder


import routes

if __name__ == '__main__':
    print("#############Starting app##############")
    app.run(host=os.environ['ANIMAL_CARDS_HOST'],
            port=os.environ['ANIMAL_CARDS_PORT'], debug=os.environ['DEBUG_MODE'])
