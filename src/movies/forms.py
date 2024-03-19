from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import Length


class MovieSearchForm(FlaskForm):
    query_string = StringField(
        "Query",
        validators=[
            Length(min=3, message="Search query must be at least 3 characters")
        ],
    )
