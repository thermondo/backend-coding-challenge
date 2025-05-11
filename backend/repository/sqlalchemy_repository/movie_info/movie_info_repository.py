from typing import List, Optional

from sqlalchemy import orm, insert

from domain_models.movie_info import MovieInfoModel
from repository.models import (
	CreateMovieInfoRequest,
	UpdateMovieInfoRequest,
)
from repository.adapter.tables.movie_info import movie_info_table
from repository.interfaces.movie_repository import MovieInfoRepository
from repository.sqlalchemy_repository.movie_info.mappers import (
	to_movie_info,
	to_movies_info,
)
from repository.sqlalchemy_repository.movie_info.queries import (
	insert_movie_info,
	select_movie_info_as_json,
	update_movie_info,
	select_movies_info,
	count_movies,
)
from repository.repository_utils import json_column


class SQLAlchemyMovieInfoRepository(MovieInfoRepository):
	def __init__(self, session: orm.Session):
		self._session = session

	def create_movie(self, request: CreateMovieInfoRequest) -> MovieInfoModel:
		insert_stmt = insert_movie_info(request)
		result = self._session.execute(insert_stmt).first()
		if result:
			return to_movie_info(result[0])
		raise ValueError('error while creating movie info object')

	def select_movies(
		self,
		query: Optional[str] = None,
		offset: int = 0,
		limit: int = 10,
	) -> List[MovieInfoModel]:
		select = select_movies_info(query).limit(limit).offset(offset)
		result = self._session.execute(select)
		return to_movies_info(result)

	def select_movie(self, movie_id: int) -> Optional[MovieInfoModel]:
		select = select_movie_info_as_json().where(movie_info_table.columns.id == movie_id)
		result = self._session.execute(select).first()
		if result:
			return to_movie_info(result[0])
		return None

	def count_movies(self, query: Optional[str] = None) -> int:
		select = count_movies(query)
		result = self._session.execute(select).first()
		return result[0]

	def update_movie(self, request: UpdateMovieInfoRequest) -> Optional[MovieInfoModel]:
		update = update_movie_info(request).where(movie_info_table.columns.id == request.id)
		if update is not None:
			result = self._session.execute(update).first()
			if result:
				return to_movie_info(result[0])
			raise ValueError('error while updating user info')
		return self.select_movie(request.id)
