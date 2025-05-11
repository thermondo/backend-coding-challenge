from typing import Any, Dict, Optional, Union

from sqlalchemy import insert, select, update, Column, ScalarSelect, func

from repository.models import (
	CreateRatingInfoRequest,
	UpdateRatingInfoRequest,
)
from repository.models import (
	CreateRatingReportRequest,
	UpdateRatingReportRequest,
)
from repository.adapter.tables.movie_info import movie_info_table
from repository.adapter.tables.rating_info import rating_info_table
from repository.adapter.tables.rating_report import rating_report_table
from repository.adapter.tables.user_info import user_info_table
from repository.sqlalchemy_repository.movie_info.queries import (
	select_movie_info_as_json,
)
from repository.sqlalchemy_repository.user_info.queries import select_user_info_as_json
from repository.repository_utils import (
	insert_into_table,
	json_column,
	select_from_table_as_json,
	update_table_rows,
	select_from,
)


def rating_info_column_as_dict(
	user_info_id: Union[int, Column],
	movie_info_id: Union[int, Column],
	resolve_relations: bool = False,
) -> Dict:
	movie_info: Union[ScalarSelect, Column] = rating_info_table.table.columns.movie_info_id
	user_info: Union[ScalarSelect, Column] = rating_info_table.table.columns.user_info_id
	if resolve_relations:
		movie_info = (
			select_movie_info_as_json()
			.where(movie_info_table.table.columns.id == movie_info_id)
			.scalar_subquery()
		)
		user_info = (
			select_user_info_as_json()
			.where(user_info_table.table.columns.id == user_info_id)
			.scalar_subquery()
		)
	return {
		'id': rating_info_table.table.columns.id,
		'movie_info': movie_info,
		'user_info': user_info,
		'review': rating_info_table.table.columns.review,
		'rating': rating_info_table.table.columns.rating,
		'active': rating_info_table.table.columns.active,
		'date_created': rating_info_table.table.columns.date_created,
		'date_updated': rating_info_table.table.columns.date_updated,
	}


def rating_report_column_as_dict(
	movie_info_id: Union[int, Column],
	resolve_relations: bool = False,
) -> Dict:
	movie_info: Union[ScalarSelect, Column] = rating_report_table.table.columns.movie_info_id
	if resolve_relations:
		movie_info = (
			select_movie_info_as_json()
			.where(movie_info_table.table.columns.id == movie_info_id)
			.scalar_subquery()
		)
	return {
		'id': rating_report_table.table.columns.id,
		'movie_info': movie_info,
		'accumulated_rating': rating_report_table.table.columns.accumulated_rating,
		'date_created': rating_report_table.table.columns.date_created,
		'date_updated': rating_report_table.table.columns.date_updated,
	}


def select_rating_info_as_json() -> select:
	return select_from_table_as_json(
		rating_info_table,
		rating_info_column_as_dict(
			rating_info_table.columns.user_info_id,
			rating_info_table.columns.movie_info_id,
			True,
		),
	)


def select_rating_report_as_json() -> select:
	return select_from_table_as_json(
		rating_report_table,
		rating_report_column_as_dict(
			rating_report_table.columns.movie_info_id,
			True,
		),
	)


def insert_rating_info(request: CreateRatingInfoRequest) -> insert:
	return insert_into_table(
		rating_info_table,
		[
			{
				'movie_info_id': request.movie_info_id,
				'user_info_id': request.user_info_id,
				'rating': request.rating,
				'review': request.review,
			}
		],
	).returning(
		json_column(rating_info_column_as_dict(request.user_info_id, request.movie_info_id, True))
	)


def insert_rating_report_entry(request: CreateRatingReportRequest) -> insert:
	return insert_into_table(
		rating_report_table,
		[
			{
				'movie_info_id': request.movie_info_id,
				'accumulated_rating': request.accumulated_rating,
			}
		],
	).returning(json_column(rating_report_column_as_dict(request.movie_info_id, True)))


def update_rating_info(request: UpdateRatingInfoRequest) -> Optional[update]:
	update_obj: Dict[str, Any] = {}
	if request.review is not None:
		update_obj['review'] = request.review
	if request.rating is not None:
		update_obj['rating'] = request.rating

	if update_obj:
		return (
			update_table_rows(
				rating_info_table,
				update_obj,
			)
			.where(rating_info_table.columns.id == request.id)
			.returning(
				json_column(
					rating_info_column_as_dict(
						rating_info_table.columns.user_info_id,
						rating_info_table.columns.movie_info_id,
						True,
					)
				)
			)
		)
	return None


def update_rating_report_entry(request: UpdateRatingReportRequest) -> Optional[update]:
	update_obj: Dict[str, Any] = {}
	if request.accumulated_rating is not None:
		update_obj['accumulated_rating'] = request.accumulated_rating

	if update_obj:
		return (
			update_table_rows(
				rating_report_table,
				update_obj,
			)
			.where(rating_report_table.columns.id == request.id)
			.returning(
				json_column(
					rating_report_column_as_dict(
						rating_report_table.columns.movie_info_id,
						True,
					)
				)
			)
		)
	return None


def select_movie_average_rating(movie_info_id: int):
	select_stmt = select_from(
		rating_info_table,
		[
			rating_info_table.columns.movie_info_id,
			func.avg(rating_info_table.columns.rating).label('average_rating'),
		],
	)

	select_stmt = select_stmt.where(
		rating_info_table.columns.movie_info_id == movie_info_id
	).group_by(rating_info_table.columns.movie_info_id)

	return select_stmt
