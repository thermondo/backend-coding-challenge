import re

from flask_wtf import FlaskForm
from wtforms import StringField, EmailField, PasswordField, ValidationError
from wtforms.validators import DataRequired, Email, EqualTo, Length

from src.users.models import User


class UsernameValidator(object):
    def __init__(self):
        self.message = ('Username may contain only lowercase letters, numbers,'
                        ' and underscores.')

    def __call__(self, form, field):
        res = bool(re.match("^[a-z0-9_]*$", field.data))
        if not res:
            raise ValidationError(self.message)


class RegisterForm(FlaskForm):
    email = EmailField(
        "Email", validators=[DataRequired(), Email(), Length(min=6, max=40)]
    )
    username = StringField(
        "Username", validators=[
            DataRequired(), UsernameValidator(), Length(min=6, max=40)]
    )
    password = PasswordField(
        "Password", validators=[DataRequired(), Length(min=6, max=25)]
    )
    confirm = PasswordField(
        "Repeat password",
        validators=[
            DataRequired(),
            EqualTo("password", message="Passwords must match."),
        ],
    )

    def validate(self, extra_validators={}):
        initial_validation = super(RegisterForm, self).validate()
        if not initial_validation:
            return False
        user = User.query.filter_by(username=self.username.data).first()
        if user:
            self.username.errors.append("Username already registered")
            return False
        if self.password.data != self.confirm.data:
            self.password.errors.append("Passwords must match")
            return False
        return True


class LoginForm(FlaskForm):
    username = StringField("Username", validators=[
        DataRequired(), UsernameValidator()])
    password = PasswordField("Password", validators=[DataRequired()])
