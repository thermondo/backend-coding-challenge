import unittest

from sqlalchemy import select

from base_test import BaseTestCase

from src import db
from src.users.models import User
from src.movies.models import Movie
from src.ratings.forms import RatingForm


class TestRatingForm(BaseTestCase):
    def test_validate_success_new_form(self):
        # Ensure valid movie info
        existing_user = db.session.scalars(
            select(User).order_by(User.id.desc()).limit(1)
        ).one()
        existing_movie = db.session.scalars(
            select(Movie).order_by(Movie.id.desc()).limit(1)
        ).one()

        form = RatingForm(
                username=existing_user.username,
                movie_id=existing_movie.id,
                rating_value=5,  # Out of 5
            )
        self.assertTrue(form.validate())

    def test_validate_rating_must_be_1_to_5(self):
        # Ensure rating over 5 will fail
        existing_user = db.session.scalars(
            select(User).order_by(User.id.desc()).limit(1)
        ).one()
        existing_movie = db.session.scalars(
            select(Movie).order_by(Movie.id.desc()).limit(1)
        ).one()

        form = RatingForm(
                username=existing_user.username,
                movie_id=existing_movie.id,
                rating_value=20,
            )
        self.assertFalse(form.validate())

    def test_validate_username(self):
        # Ensure rating over 5 will fail
        existing_movie = db.session.scalars(
            select(Movie).order_by(Movie.id.desc()).limit(1)
        ).one()

        form = RatingForm(
                username="randomusername",
                movie_id=existing_movie.id,
                rating_value=5,
            )
        self.assertFalse(form.validate())

    def test_validate_movie_id(self):
        # Ensure rating over 5 will fail
        existing_user = db.session.scalars(
            select(User).order_by(User.id.desc()).limit(1)
        ).one()

        form = RatingForm(
                username=existing_user.username,
                movie_id=1000,
                rating_value=5,
            )
        self.assertFalse(form.validate())


if __name__ == "__main__":
    unittest.main()
