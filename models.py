from flask_login import UserMixin
from peewee import IntegerField, Model, TextField, SqliteDatabase
from werkzeug.security import generate_password_hash

db = SqliteDatabase('people.db')


class BaseModel(Model):
    class Meta:
        database = db


class User(BaseModel, UserMixin):
    id = IntegerField(primary_key=True)
    login = TextField(unique=True)
    password = TextField()


if __name__ == "__main__":
    db.drop_tables([User])
    db.create_tables([User])
    User(login="admin", password=generate_password_hash("1234")).save()
