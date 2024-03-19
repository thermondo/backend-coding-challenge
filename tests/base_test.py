import os

from flask_testing import TestCase
from sqlalchemy_utils import database_exists, create_database

from src import app, db
from src.users.models import User
from src.movies.models import Movie
from src.ratings.models import Rating


class BaseTestCase(TestCase):
    def create_app(self):
        app.config.from_object("config.TestingConfig")
        return app

    def setUp(self):
        if not database_exists(app.config['SQLALCHEMY_DATABASE_URI']):
            create_database(app.config['SQLALCHEMY_DATABASE_URI'])
        db.create_all()
        self.__create_test_data()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        os.remove(app.config['TEST_DATABASE_FILE_PATH'])

    def __create_test_data(self):
        # Test user
        user1 = User(
            username="unittester",
            email="ut@est.com",
            password="unit_tester",
        )
        user2 = User(
            username="onemoreuser",
            email="anotherut@est.com",
            password="unit_tester",
        )
        # Test movie
        movie1 = Movie(
            tmdb_id=634492,
            title='Test title: Madam Web',
            release_date='2024-03-19',
            poster_path='/rULWuutDcN5NvtiZi4FRPzRYWSh.jpg',
            overview=('Forced to confront revelations about her past, '
                      'paramedic Cassandra Webb forges a relationship with '
                      'three young women destined for powerful futures...if '
                      'they can all survive a deadly present.'),
        )
        movie2 = Movie(
            tmdb_id=1046090,
            title='Another title: The Pig, the Snake and the Pigeon',
            release_date='2023-10-06',
            poster_path='/7IJ7F8tX7IAkpUdaGovOBJqORnJ.jpg',
            overview=('The arrogant, third most-wanted criminal in Taiwan, '
                      'decides to get rid of the top two competitors and '
                      'crowns himself the most-wanted criminal before dying.'),
        )
        # Save the users and movies to get their IDs
        db.session.add(user1)
        db.session.add(user2)
        db.session.add(movie1)
        db.session.add(movie2)
        db.session.commit()
        # Now create ratings
        rating = Rating(
            movie_id=movie1.id,
            user_id=user1.id,
            value=5,
            review="I love this movie",
        )
        db.session.add(rating)
        db.session.commit()
