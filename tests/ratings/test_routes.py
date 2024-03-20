import unittest

from base_test import BaseTestCase

from src import db
from src.users.models import User
from src.movies.models import Movie
from src.ratings.models import Rating


class TestNewRating(BaseTestCase):
    def test_new_rating_creation(self):
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

        with self.client:
            self.client.post(
                "/login",
                data=dict(username="justforthistest", password="unit_test"),
                follow_redirects=True,
            )
            rating_value = 5
            rating_review_text = "I love this movie"
            response = self.client.post(
                "/ratings/new",
                data=dict(
                    movie_id=new_movie.id,
                    username=new_user.username,
                    rating_value=rating_value,
                    review=rating_review_text,
                ),
                follow_redirects=True,
            )
            # import pdb; pdb.set_trace()
        rating = Rating.query.filter_by(user_id=new_user.id).first()
        self.assertTrue(rating and rating.id)  # Made it to the DB!
        # Redirect back to movie page
        self.assertIn(new_movie.title.encode(), response.data)


if __name__ == "__main__":
    unittest.main()
