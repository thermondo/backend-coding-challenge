import os

from flask_testing import TestCase
from sqlalchemy_utils import database_exists, create_database

from src import app, db
from src.users.models import User
from src.movies.models import Movie


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
        user = User(
            username="unittester",
            email="ut@est.com",
            password="unit_tester",
        )
        # Test movie
        movie = Movie(
            tmdb_id=634492,
            title='Test title: Madam Web',
            release_date='2024-03-19',
            poster_path='/rULWuutDcN5NvtiZi4FRPzRYWSh.jpg',
            overview=('Forced to confront revelations about her past, '
                'paramedic Cassandra Webb forges a relationship with '
                'three young women destined for powerful futures...if '
                'they can all survive a deadly present.')
        )
        # Test rating
        # TODO
        db.session.add(user)
        db.session.add(movie)
        db.session.commit()
