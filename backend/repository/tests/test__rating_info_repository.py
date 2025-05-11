from decimal import Decimal

from domain_models.rating_info import RatingInfoModel
from domain_models.rating_report import RatingReportModel
from repository.models import CreateRatingInfoRequest
from repository.adapter.tables.rating_info import rating_info_table
from repository.sqlalchemy_repository.rating.rating_repository import (
	SQLAlchemyRatingRepository,
)
from repository.tests.fixtures.rating_data import (
	add_movies_test_data,
	add_users_test_data,
)


def test__when_rating_info_create_request_is_valid_then_insert_rating_info(
	database_session, insert_rows
) -> None:
	movies_info = add_movies_test_data(insert_rows, 5)
	users_info = add_users_test_data(insert_rows, 1)

	expected_rating_info_model = RatingInfoModel(
		rating=2,
		movie=movies_info[0],
		user=users_info[0],
		id=1,
	)

	repo = SQLAlchemyRatingRepository(database_session)
	repo.create_rating_info(
		CreateRatingInfoRequest(
			rating=2,
			movie_info_id=1,
			user_info_id=1,
		)
	)
	result = repo.select_rating_info(rating_info_id=1)

	assert result is not None
	assert result.rating == expected_rating_info_model.rating
	assert result.movie.id == expected_rating_info_model.movie.id
	assert result.user.id == expected_rating_info_model.user.id


def test__when_rating_report_create_request_is_valid_then_insert_rating_report(
	database_session, insert_rows
) -> None:
	movies_info = add_movies_test_data(insert_rows, 5)

	expected_rating_report_model = RatingReportModel(
		accumulated_rating=Decimal(0),
		movie=movies_info[0],
		id=1,
	)

	repo = SQLAlchemyRatingRepository(database_session)
	repo.redis_client.flushdb()
	repo.create_rating_report_entry(
		movie_info_id=1,
	)
	result = repo.select_rating_report_entry(rating_report_id=1)

	assert result is not None
	assert result.accumulated_rating == expected_rating_report_model.accumulated_rating
	assert result.movie.id == expected_rating_report_model.movie.id


def test__when_list_of_rating_info_for_user_is_requested_then_return_paginated_report(
	database_session, insert_rows
) -> None:
	add_movies_test_data(insert_rows, 5)
	add_users_test_data(insert_rows, 2)
	rows = [
		{
			'movie_info_id': 1,
			'user_info_id': 1,
			'rating': 2,
		},
		{
			'movie_info_id': 2,
			'user_info_id': 1,
			'rating': 4,
		},
		{
			'movie_info_id': 3,
			'user_info_id': 2,
			'rating': 3,
		},
		{
			'movie_info_id': 4,
			'user_info_id': 2,
			'rating': 2,
		},
		{
			'movie_info_id': 5,
			'user_info_id': 1,
			'rating': 1,
		},
	]
	insert_rows(rows, rating_info_table.table)

	repo = SQLAlchemyRatingRepository(database_session)
	result = repo.select_rating_info_for_user(user_info_id=1)
	assert len(result) == 3
