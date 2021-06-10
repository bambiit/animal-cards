from app import app
from models import User


@app.route('/users', methods=['GET'])
def get_users():
    return User.objects.all()
