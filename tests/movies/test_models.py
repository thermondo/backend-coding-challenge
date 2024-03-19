import unittest
from unittest.mock import patch

from base_test import BaseTestCase

from src.movies.models import Movie
from src.movies.integrations.tmdb import TmdbIntegration

from tests.mocks.tmdb import search_response_dict


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
            Movie.search_by_query_string(query_string)
            self.fail("Error was not raised")
        except ValueError as e:
            self.assertTrue(e.args[0] == "Query string cannot be empty")

    def test_search_by_query_string_tmdb(self):
        # Ensure that calling TMDB returns the results as Movie objects
        query_string = "Test"
        # Mock the call to TMDB
        with patch.object(
                TmdbIntegration,
                'search_movies',
                return_value=search_response_dict) as mock_method:
            result = Movie.search_by_query_string_tmdb(query_string)

        mock_method.assert_called_once_with(query_string)
        self.assertTrue(len(result) == len(search_response_dict['results']))
        self.assertTrue(
            result[0].title == search_response_dict['results'][0]['title'])


if __name__ == "__main__":
    unittest.main()
