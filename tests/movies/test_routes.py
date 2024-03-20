import unittest
from unittest.mock import patch
from flask_login import current_user
from sqlalchemy import select

from base_test import BaseTestCase

from src import db
from src.movies.models import Movie
from src.movies.integrations.tmdb import TmdbIntegration

from tests.mocks.tmdb import search_response_dict
from tests.mocks.tmdb import movie_details_dict


class TestMovieSearch(BaseTestCase):
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


class TestMovieShow(BaseTestCase):
    def test_show_is_accessible_without_login(self):
        # Show for a movie should be accessible without being logged in
        with self.client:
            self.client.get("/logout", follow_redirects=True)  # Make sure
            existing_movie = db.session.scalars(
                select(Movie).order_by(Movie.id.desc()).limit(1)
            ).one()
            response = self.client.get(
                f"/movies/{existing_movie.id}", follow_redirects=True)
            self.assertFalse(current_user.is_active)
            self.assertIn(f"{existing_movie.title}".encode(), response.data)


class TestMovieNew(BaseTestCase):
    def test_new_movie_creation(self):
        with self.client:
            self.client.post(
                "/login",
                data=dict(username="unittester", password="unit_tester"),
                follow_redirects=True,
            )
            new_movie_title = "This is a title"
            response = self.client.post(
                "/movies/new",
                data=dict(
                    title=new_movie_title,
                    release_date="2024-03-20",
                ),
                follow_redirects=True,
            )
        movie = Movie.query.filter_by(title=new_movie_title).first()
        self.assertTrue(movie and movie.id)  # Made it to the DB!
        self.assertIn(new_movie_title.encode(), response.data)

    def test_new_movie_creation_calls_tmdb(self):
        with patch.object(
                TmdbIntegration,
                'movie_details',
                return_value=movie_details_dict) as mock_method:
            with self.client:
                self.client.get("/logout", follow_redirects=True)
                self.client.post(
                    "/login",
                    data=dict(username="unittester", password="unit_tester"),
                    follow_redirects=True,
                )
                new_movie_title = "Kung Fu Panda 4"
                tmdb_id = 1011985
                response = self.client.post(
                    "/movies/new",
                    data=dict(
                        title=new_movie_title,
                        release_date="2024-03-20",
                        tmdb_id=tmdb_id,
                    ),
                    follow_redirects=True,
                )
        movie = Movie.query.filter_by(tmdb_id=tmdb_id).first()
        self.assertTrue(movie and movie.id)  # Made it to the DB!
        mock_method.assert_called_once_with(tmdb_id)
        self.assertIn(new_movie_title.encode(), response.data)

    def test_new_movie_creation_succeeds_when_tmdb_fails(self):
        with patch.object(
                TmdbIntegration,
                'movie_details',
                return_value={}) as mock_method:
            with self.client:
                self.client.get("/logout", follow_redirects=True)
                self.client.post(
                    "/login",
                    data=dict(username="unittester", password="unit_tester"),
                    follow_redirects=True,
                )
                new_movie_title = "This is another title"
                tmdb_id = 1  # Valid in but returns no results from TMDB
                response = self.client.post(
                    "/movies/new",
                    data=dict(
                        title=new_movie_title,
                        release_date="2024-03-20",
                        tmdb_id=tmdb_id,
                    ),
                    follow_redirects=True,
                )
        movie = Movie.query.filter_by(title=new_movie_title).first()
        self.assertTrue(movie and movie.id)  # Made it to the DB!
        mock_method.assert_called_once_with(tmdb_id)
        self.assertIn(new_movie_title.encode(), response.data)


if __name__ == "__main__":
    unittest.main()
