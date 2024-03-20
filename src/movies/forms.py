import re

from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, TextAreaField, ValidationError
from wtforms.validators import DataRequired, Length, Optional

from src.movies.models import Movie


class MovieSearchForm(FlaskForm):
    query_string = StringField(
        "Query",
        validators=[
            DataRequired(),
            Length(
                min=3, message="Search query must be at least 3 characters"),
        ],
    )


class ReleaseDateValidator(object):
    def __init__(self):
        self.message = ('Release date must be in the format YYYY-MM-DD.')

    def __call__(self, form, field):
        res = bool(re.match(r'^[0-9]{4}-[0-9]{2}-[0-9]{2}$', field.data))
        if not res:
            raise ValidationError(self.message)


class NewMovieForm(FlaskForm):
    title = StringField("Title", validators=[DataRequired()])
    release_date = StringField(
        "Release Date YYYY-MM-DD",
        validators=[DataRequired(), ReleaseDateValidator()])
    overview = TextAreaField(
        "Optional: Movie overview", validators=[Optional()])
    # TODO: Would it be better for this to be a URL?
    tmdb_id = IntegerField("Optional: TMDB ID", validators=[Optional()])

    def validate(self, extra_validators={}):
        initial_validation = super(NewMovieForm, self).validate()
        if not initial_validation:
            return False
        movie = Movie.get_by_tmdb_id(self.tmdb_id.data)
        if movie:
            self.movie_id.errors.append(
                "A movie with that TMDB ID already exists in our database!")
            return False
        return True
