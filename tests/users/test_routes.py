import unittest

from sqlalchemy import select
from flask_login import current_user

from base_test import BaseTestCase

from src import db
from src.users.models import User


class TestPublic(BaseTestCase):
    def test_main_route_requires_login(self):
        # Ensure main route requres logged in user.
        response = self.client.get("/", follow_redirects=True)
        self.assertTrue(response.status_code == 200)
        self.assertIn(b"Please log in to access this page", response.data)

    def test_logout_route_requires_login(self):
        # Ensure logout route requres logged in user.
        response = self.client.get("/logout", follow_redirects=True)
        self.assertIn(b"Please log in to access this page", response.data)


class TestUserRegistration(BaseTestCase):
    def test_user_registration(self):
        # Ensure user registration behaves correctly.
        with self.client:
            self.client.get("/logout", follow_redirects=True)
            self.client.post(
                "/register",
                data=dict(
                    email="test@user.com",
                    username="testmeok",
                    password="test_user",
                    confirm="test_user",
                ),
                follow_redirects=True,
            )
            user = User.query.filter_by(email="test@user.com").first()
            self.assertTrue(user.id)
            self.assertTrue(user.email == "test@user.com")


class TestLoggingInOut(BaseTestCase):
    def test_correct_login(self):
        # Ensure login behaves correctly with correct credentials
        with self.client:
            response = self.client.post(
                "/login",
                data=dict(username="unittester", password="unit_tester"),
                follow_redirects=True,
            )
            self.assertTrue(current_user.username == "unittester")
            self.assertTrue(current_user.is_active)
            self.assertTrue(response.status_code == 200)

    def test_logout_behaves_correctly(self):
        # Ensure logout behaves correctly, regarding the session
        with self.client:
            self.client.post(
                "/login",
                data=dict(username="unittester", password="unit_tester"),
                follow_redirects=True,
            )
            response = self.client.get("/logout", follow_redirects=True)
            self.assertIn(b"You were logged out.", response.data)
            self.assertFalse(current_user.is_active)


class TestUserProfile(BaseTestCase):
    def test_show(self):
        # Show for a username should be accessible without being logged in
        with self.client:
            existing_user = db.session.scalars(
                select(User).order_by(User.id.desc()).limit(1)
            ).one()
            username = existing_user.username
            response = self.client.get(
                f"/users/{username}", follow_redirects=True)
            self.assertFalse(current_user.is_active)
            self.assertIn(
                f"{username}'s Ratings and Reviews".encode(), response.data)


if __name__ == "__main__":
    unittest.main()
