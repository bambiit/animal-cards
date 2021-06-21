from enum import Enum

class UserType(Enum):
  ADMIN = 1
  AUTHENTICATED_USER = 2
  NOT_ALLOWED_USER = 3