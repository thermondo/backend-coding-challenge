import unittest
from unittest.mock import patch

from base_test import BaseTestCase

from src.movies.integrations.tmdb import TmdbIntegration

from tests.mocks.tmdb import search_response_dict


class TestSearch(BaseTestCase):

    def test_search_with_query(self):
        # Ensure that the search page returns results
        # Mock the call to TMDB
        with patch.object(
                TmdbIntegration,
                'search_movies',
                return_value=search_response_dict) as mock_method:
            with self.client:
                query_string = "Test"
                response = self.client.post(
                    "/search",
                    data=dict(query_string=query_string),
                    follow_redirects=True,
                )

        mock_method.assert_called_once_with(query_string)
        self.assertIn(b"Test title: Madam Web", response.data)


if __name__ == "__main__":
    unittest.main()
