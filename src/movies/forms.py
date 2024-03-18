import re

from flask_wtf import FlaskForm
from wtforms import StringField, EmailField, PasswordField, ValidationError
from wtforms.validators import DataRequired, Email, EqualTo, Length

from src.users.models import User


class MovieSearchForm(FlaskForm):
    query_string = StringField(
        "Query",
        validators=[
            Length(min=3, message="Search query must be at least 3 characters")
        ],
    )
