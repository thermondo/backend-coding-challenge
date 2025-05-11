from typing import Any, Dict, Optional

from sqlalchemy import desc, func
from sqlalchemy.sql import select, insert, update
from repository.models import (
	UpdateMovieInfoRequest,
	CreateMovieInfoRequest,
)
from repository.adapter.tables.movie_info import movie_info_table
from repository.repository_utils import (
	insert_into_table,
	json_column,
	select_from_table_as_json,
	update_table_rows,
	select_from,
)


def movie_info_column_as_dict() -> Dict:
	return {
		'id': movie_info_table.table.columns.id,
		'title': movie_info_table.table.columns.title,
		'active': movie_info_table.table.columns.active,
		'description': movie_info_table.table.columns.description,
		'release_year': movie_info_table.table.columns.release_year,
		'date_created': movie_info_table.table.columns.date_created,
		'date_updated': movie_info_table.table.columns.date_updated,
	}


def select_movies_info(query: Optional[str] = None) -> select:
	select = select_from(
		movie_info_table,
		[
			movie_info_table.columns.id,
			movie_info_table.columns.title,
			movie_info_table.columns.description,
			movie_info_table.columns.release_year,
			movie_info_table.columns.active,
			movie_info_table.columns.date_created,
			movie_info_table.columns.date_updated,
		],
	)
	return select.where(
		movie_info_table.columns.name.ilike(f'%{query}%') if query else True
	).order_by(desc(movie_info_table.columns.id))


def select_movie_info_as_json() -> select:
	return select_from_table_as_json(movie_info_table, movie_info_column_as_dict())


def insert_movie_info(request: CreateMovieInfoRequest) -> insert:
	insert_stmt = insert_into_table(
		movie_info_table,
		[
			{
				'title': request.title,
				'description': request.description,
				'release_year': request.release_year,
			}
		],
	).returning(json_column(movie_info_column_as_dict()))
	return insert_stmt


def update_movie_info(request: UpdateMovieInfoRequest) -> Optional[update]:
	update_obj: Dict[str, Any] = {}

	if request.active is not None:
		update_obj['active'] = request.active
	if request.release_year is not None:
		update_obj['release_year'] = request.release_year
	if request.description is not None:
		update_obj['description'] = request.description
	if request.title is not None:
		update_obj['title'] = request.title

	if update_obj:
		return update_table_rows(movie_info_table, update_obj).returning(
			json_column(movie_info_column_as_dict())
		)
	return None


def count_movies(query: Optional[str]) -> select:
	select = select_from(
		movie_info_table,
		[
			func.count().label('count'),
		],  # pylint: disable=E1102
	)
	if query:
		return select.where(movie_info_table.columns.name.ilike(f'%{query}%'))
	return select
