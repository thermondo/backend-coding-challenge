import unittest

from base_test import BaseTestCase

from src.movies.forms import MovieSearchForm, NewMovieForm


class TestMovieSearchForm(BaseTestCase):
    def test_validate_success_search_form(self):
        # Ensure valid query is valid
        form = MovieSearchForm(query_string="This is a test")
        self.assertTrue(form.validate())

    def test_validate_query_cannot_be_blank(self):
        # Ensure blank query is not valid
        form = MovieSearchForm(query_string="")
        self.assertFalse(form.validate())


class TestMovieNewForm(BaseTestCase):
    def test_validate_success_new_form(self):
        # Ensure valid movie info
        form = NewMovieForm(
                title="This is a title",
                release_date="2024-03-20",
            )
        self.assertTrue(form.validate())

    def test_validate_title_and_date_cannot_be_blank(self):
        # Ensure blank title and date fail
        form = NewMovieForm(
                title="",
                release_date="",
            )
        self.assertFalse(form.validate())

    def test_validate_date_must_have_format_YYYYMMDD(self):
        # Ensure bad date formatting fails
        form = NewMovieForm(
                title="This is a title",
                release_date="3/20/2024",
            )
        self.assertFalse(form.validate())


if __name__ == "__main__":
    unittest.main()
