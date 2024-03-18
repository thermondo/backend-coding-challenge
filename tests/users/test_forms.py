import unittest

from base_test import BaseTestCase

from src.users.forms import LoginForm, RegisterForm


class TestRegisterForm(BaseTestCase):
    def test_validate_success_register_form(self):
        # Ensure correct data validates.
        form = RegisterForm(
            email="new@test.com",
            username="newtest",
            password="example",
            confirm="example",
        )
        self.assertTrue(form.validate())

    def test_validate_invalid_password_format(self):
        # Ensure incorrect data does not validate.
        form = RegisterForm(
            email="new@test.com",
            username="newtest",
            password="example",
            confirm="",
        )
        self.assertFalse(form.validate())

    def test_validate_email_already_registered(self):
        # Ensure user can't register when a duplicate email is used
        form = RegisterForm(
            email="ut@est.com",
            username="anothertest",
            password="unit_tester",
            confirm="unit_tester",
        )
        self.assertFalse(form.validate())

    def test_validate_email_already_registered(self):
        # Ensure user can't register when a duplicate username is used
        form = RegisterForm(
            email="anothert@est.com",
            username="unittester",
            password="unit_tester",
            confirm="unit_tester",
        )
        self.assertFalse(form.validate())


class TestLoginForm(BaseTestCase):
    def test_validate_success_login_form(self):
        # Ensure correct data validates.
        form = LoginForm(username="unittester", password="unit_tester")
        self.assertTrue(form.validate())

    def test_validate_invalid_email_format(self):
        # Ensure invalid email format throws error.
        form = LoginForm(email="unknown", password="example")
        self.assertFalse(form.validate())


if __name__ == "__main__":
    unittest.main()
