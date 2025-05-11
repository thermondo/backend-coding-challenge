from time import time

from domain_models.movie_info import MovieInfoModel
from repository.models import (
    CreateMovieInfoRequest,
    UpdateMovieInfoRequest,
)
from repository.adapter.tables.movie_info import movie_info_table
from repository.sqlalchemy_repository.movie_info.movie_info_repository import (
    SQLAlchemyMovieInfoRepository,
)
from utils import from_timestamp


def test__when_movie_info_create_request_is_valid_then_insert_movie_info(
    database_session,
) -> None:
    expected_movie_info_model = MovieInfoModel(
        title='movie1',
        active=True,
        release_year='2007',
        id=1,
    )

    repo = SQLAlchemyMovieInfoRepository(database_session)
    repo.create_movie(
        CreateMovieInfoRequest(
            title='movie1',
            release_year='2007',
        )
    )
    result = repo.select_movie(movie_id=1)

    assert result is not None
    assert result.title == expected_movie_info_model.title
    assert result.release_year == expected_movie_info_model.release_year
    assert result.id == expected_movie_info_model.id
    assert result.active == expected_movie_info_model.active
    assert result.description is None


def test__when_movie_info_is_exists_then_return_valid_movie_info(
    insert_rows, database_session
) -> None:
    time_stamp = int(time() * 1000)
    rows = [
        {
            'title': 'name1',
            'description': 'description',
            'date_created': time_stamp,
            'date_updated': time_stamp,
            'active': True,
        }
    ]
    insert_rows(rows, movie_info_table.table)

    repo = SQLAlchemyMovieInfoRepository(database_session)
    result = repo.select_movie(movie_id=1)

    assert result is not None

    expected_movie_info_model = MovieInfoModel(
        title='name1',
        active=True,
        description='description',
        id=1,
        date_created=from_timestamp(time_stamp),
        date_updated=from_timestamp(time_stamp),
    )

    assert result == expected_movie_info_model


def test__when_movies_list_is_requested_then_return_paginated_movies_list(
    insert_rows, database_session
) -> None:
    time_stamp = int(time() * 1000)
    rows = [
        {
            'title': 'name1',
            'description': 'description',
            'date_created': time_stamp,
            'date_updated': time_stamp,
            'active': True,
        },
        {
            'title': 'name2',
            'description': 'description',
            'date_created': time_stamp,
            'date_updated': time_stamp,
            'active': True,
        },
    ]
    insert_rows(rows, movie_info_table.table)

    repo = SQLAlchemyMovieInfoRepository(database_session)
    result = repo.select_movies()

    assert result is not None

    expected_movie_info_model_1 = MovieInfoModel(
        title='name1',
        active=True,
        description='description',
        id=1,
        date_created=from_timestamp(time_stamp),
        date_updated=from_timestamp(time_stamp),
    )
    expected_movie_info_model_2 = MovieInfoModel(
        title='name2',
        active=True,
        description='description',
        id=2,
        date_created=from_timestamp(time_stamp),
        date_updated=from_timestamp(time_stamp),
    )

    assert result == [expected_movie_info_model_2, expected_movie_info_model_1]


def test__when_update_is_called_with_valid_update_request_then_update_movie_info(
    insert_rows, database_session
) -> None:
    rows = [{'title': 'title1', 'release_year': '2007', 'active': True}]
    insert_rows(rows, movie_info_table.table)
    repo = SQLAlchemyMovieInfoRepository(database_session)
    repo.update_movie(UpdateMovieInfoRequest(id=1, active=False))
    result = repo.select_movie(movie_id=1)

    assert result is not None
    assert not result.active


def test__when_movies_list_count_is_requested_then_return_expected_result(
    insert_rows, database_session
) -> None:
    time_stamp = int(time() * 1000)
    rows = [
        {
            'title': 'name1',
            'description': 'description',
            'date_created': time_stamp,
            'date_updated': time_stamp,
            'active': True,
        },
        {
            'title': 'name2',
            'description': 'description',
            'date_created': time_stamp,
            'date_updated': time_stamp,
            'active': True,
        },
    ]
    insert_rows(rows, movie_info_table.table)

    repo = SQLAlchemyMovieInfoRepository(database_session)
    result = repo.count_movies()

    assert result is not None
    assert result == 2
