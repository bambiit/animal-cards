from pymodm import MongoModel, fields


class User(MongoModel):
    username: fields.CharField(primary_key=True, required=True)
    email: fields.EmailField(unique=True, required=True)
    first_name: fields.CharField()
    last_name: fields.CharField()
    hashed_password: fields.CharField()
