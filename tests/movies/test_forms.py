import unittest

from base_test import BaseTestCase

from src.movies.forms import MovieSearchForm


class TestMovieSearchForm(BaseTestCase):
    def test_validate_success_search_form(self):
        # Ensure valid query is valid
        form = MovieSearchForm(query_string="This is a test")
        self.assertTrue(form.validate())

    def test_validate_query_cannot_be_blank(self):
        # Ensure blank query is not valid
        form = MovieSearchForm(query_string="")
        self.assertFalse(form.validate())


if __name__ == "__main__":
    unittest.main()
