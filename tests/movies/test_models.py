import datetime
import unittest

from base_test import BaseTestCase

from src.movies.models import Movie


class TestMovie(BaseTestCase):

    def test_search_by_query_string_valid_query(self):
        # Ensure that existing movies are discovered by query string
        query_string = "Test"
        result = Movie.search_by_query_string(query_string)
        self.assertTrue(len(result) > 0)
        self.assertTrue(query_string in result[0].title)

    def test_search_by_query_string_blank_query(self):
        # Ensure that a blank query string raises an exception
        query_string = ""
        try:
            result = Movie.search_by_query_string(query_string)
            self.fail("Error was not raised")
        except ValueError as e:
            self.assertTrue(e.args[0] == "Query string cannot be empty")

    # TODO test the integration

if __name__ == "__main__":
    unittest.main()
