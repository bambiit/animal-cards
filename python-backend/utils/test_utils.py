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
    card_model = User()
    return card_model.add_many(TestUtils.INITIAL_USERS)


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
    return user_model.count()['num_of_users']