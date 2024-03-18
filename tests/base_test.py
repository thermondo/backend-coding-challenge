import os

from flask_testing import TestCase
from sqlalchemy_utils import database_exists, create_database

from src import app, db
from src.users.models import User


class BaseTestCase(TestCase):
    def create_app(self):
        app.config.from_object("config.TestingConfig")
        return app

    def setUp(self):
        if not database_exists(app.config['SQLALCHEMY_DATABASE_URI']):
            create_database(app.config['SQLALCHEMY_DATABASE_URI'])
        db.create_all()
        user = User(
            username="unittester",
            email="ut@est.com",
            password="unit_tester",
        )
        db.session.add(user)
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        os.remove(app.config['TEST_DATABASE_FILE_PATH'])
