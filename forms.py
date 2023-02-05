from flask_login import UserMixin
from flask_wtf import FlaskForm
from werkzeug.security import check_password_hash
from wtforms import PasswordField, StringField, validators

from models import User


class LoginForm(FlaskForm, UserMixin):
    login = StringField()
    password = PasswordField()

    def validate_login(self, field):
        cur_user = self.get_user()
        if cur_user is None:
            raise validators.ValidationError("Invalid user")
        if not check_password_hash(cur_user.password, self.password.data):
            raise validators.ValidationError("Invalid password")

    def get_user(self):
        users = [e for e in User.select().where(User.login == self.login.data)]
        if users:
            return users[0]
        else:
            return None
