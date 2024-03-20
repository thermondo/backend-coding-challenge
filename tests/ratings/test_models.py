import unittest

from base_test import BaseTestCase

from sqlalchemy import select

from src import db
from src.ratings.models import Rating
from src.users.models import User
from src.movies.models import Movie


class TestRating(BaseTestCase):

    def test_create_and_save(self):
        # Create and save a new rating successfully
        rating_value = 5
        rating_review_text = "I love this movie"
        new_movie = Movie(
                title="Movie just for this test",
                release_date="2024-03-19",
            )
        new_user = User(
            username="justforthistest",
            email="justforthist@est.com",
            password="unit_test",
            )
        db.session.add_all([new_movie, new_user])
        db.session.commit()
        # Make a new rating object
        new_rating = Rating.create_and_save(
            new_movie.id, new_user.id, rating_value, rating_review_text)

        self.assertTrue(new_rating.id > 0)
        self.assertIsNotNone(db.session.get(Rating, new_rating.id))

    def test_get_all_by_movie(self):
        existing_rating = db.session.scalars(
            select(Rating).order_by(Rating.id.desc()).limit(1)
        ).one()
        ratings_from_movie = Rating.get_all_by_movie(existing_rating.movie_id)
        self.assertTrue(len(ratings_from_movie) > 0)
        self.assertTrue(
            existing_rating.id in [r.id for r in ratings_from_movie])

    def test_get_all_by_user(self):
        existing_rating = db.session.scalars(
            select(Rating).order_by(Rating.id.desc()).limit(1)
        ).one()
        ratings_from_user = Rating.get_all_by_user(existing_rating.user_id)
        self.assertTrue(len(ratings_from_user) > 0)
        self.assertTrue(
            existing_rating.id in [r.id for r in ratings_from_user])


if __name__ == "__main__":
    unittest.main()
