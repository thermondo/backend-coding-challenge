from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, TextAreaField
from wtforms.validators import DataRequired, NumberRange

from src import db
from src.users.models import User
from src.movies.models import Movie


class RatingForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    movie_id = IntegerField("Movie ID", validators=[DataRequired()])
    rating_value = IntegerField("Rating", validators=[
        DataRequired(), NumberRange(
            min=1,
            max=5,
            message="Rating must be a number between 1 👎 and 5 👍")])
    review = TextAreaField("Optional review")

    def validate(self, extra_validators={}):
        initial_validation = super(RatingForm, self).validate()
        if not initial_validation:
            return False
        # TODO: Validate that the user is logged in
        user = User.get_by_username(self.username.data)
        if not user:
            self.username.errors.append("User does not exist")
            return False
        movie = db.session.get(Movie, self.movie_id.data)
        if not movie:
            self.movie_id.errors.append("Movie does not exist")
            return False
        return True
