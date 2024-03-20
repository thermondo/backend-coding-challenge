import datetime
import unittest

from base_test import BaseTestCase
from flask_login import current_user
from sqlalchemy import select

from src import bcrypt, db
from src.users.models import User


class TestUser(BaseTestCase):
    def test_get_by_username(self):
        existing_user = db.session.scalars(select(User).limit(1)).one()
        user_from_username = User.get_by_username(existing_user.username)
        self.assertTrue(user_from_username.id == existing_user.id)

    def test_login(self):
        # Ensure id is correct for the current/logged in user
        with self.client:
            self.client.get("/logout", follow_redirects=True)
            self.client.post(
                "/login",
                data=dict(username="unittester", password="unit_tester"),
                follow_redirects=True,
            )
            self.assertTrue(current_user.id == 1)

    def test_created_at_defaults_to_datetime(self):
        # Ensure that registered_on is a datetime
        with self.client:
            self.client.get("/logout", follow_redirects=True)
            self.client.post(
                "/login",
                data=dict(username="unittester", password="unit_tester"),
                follow_redirects=True,
            )
            user = User.query.filter_by(username="unittester").first()
            self.assertIsInstance(user.created_at, datetime.datetime)

    def test_check_password(self):
        # Ensure given password is correct after unhashing
        user = User.query.filter_by(username="unittester").first()
        self.assertTrue(
            bcrypt.check_password_hash(user.password, "unit_tester"))
        self.assertFalse(bcrypt.check_password_hash(user.password, "foobar"))

    def test_validate_invalid_password(self):
        # Ensure user can't login when the pasword is incorrect
        with self.client:
            self.client.get("/logout", follow_redirects=True)
            response = self.client.post(
                "/login",
                data=dict(username="unittester", password="foo_bar"),
                follow_redirects=True,
            )
        self.assertIn(b"Invalid username and/or password.", response.data)


if __name__ == "__main__":
    unittest.main()
