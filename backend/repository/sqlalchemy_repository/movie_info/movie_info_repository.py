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


class SQLAlchemyMovieInfoRepository(MovieInfoRepository):
	def __init__(self, session: orm.Session):
		"""
		Initialize the repository with a SQLAlchemy session.

		Parameters:
		    session (orm.Session): SQLAlchemy session object for database interactions.
		"""
		self._session = session

	def create_movie(self, request: CreateMovieInfoRequest) -> MovieInfoModel:
		"""
		Create a new movie entry in the database.

		Parameters:
		    request (CreateMovieInfoRequest): The request object containing movie details.

		Returns:
		    MovieInfoModel: The created MovieInfoModel object.

		Raises:
		    ValueError: If the movie creation fails.
		"""
		insert_stmt = insert_movie_info(request)
		result = self._session.execute(insert_stmt).first()
		if result:
			return to_movie_info(result[0])
		raise ValueError('Error while creating movie info object')

	def select_movies(
		self,
		query: Optional[str] = None,
		offset: int = 0,
		limit: int = 10,
	) -> List[MovieInfoModel]:
		"""
		Retrieve a list of movie records with optional query filtering and pagination.

		Parameters:
		    query (Optional[str]): A query string to filter movies.
		    offset (int): Number of records to skip (default is 0).
		    limit (int): Maximum number of records to return (default is 10).

		Returns:
		    List[MovieInfoModel]: A list of MovieInfoModel objects.
		"""
		select = select_movies_info(query).limit(limit).offset(offset)
		result = self._session.execute(select)
		return to_movies_info(result)

	def select_movie(self, movie_id: int) -> Optional[MovieInfoModel]:
		"""
		Retrieve a specific movie record by its ID.

		Parameters:
		    movie_id (int): The ID of the movie to retrieve.

		Returns:
		    Optional[MovieInfoModel]: The MovieInfoModel object if found, otherwise None.
		"""
		select = select_movie_info_as_json().where(movie_info_table.columns.id == movie_id)
		result = self._session.execute(select).first()
		if result:
			return to_movie_info(result[0])
		return None

	def count_movies(self, query: Optional[str] = None) -> int:
		"""
		Count the total number of movies, optionally filtered by a query string.

		Parameters:
		    query (Optional[str]): A query string to filter movies.

		Returns:
		    int: The count of movies.
		"""
		select = count_movies(query)
		result = self._session.execute(select).first()
		return result[0]

	def update_movie(self, request: UpdateMovieInfoRequest) -> Optional[MovieInfoModel]:
		"""
		Update an existing movie entry in the database.

		Parameters:
		    request (UpdateMovieInfoRequest): The update object containing movie details to be updated.

		Returns:
		    Optional[MovieInfoModel]: The updated MovieInfoModel object if successful, otherwise None.

		Raises:
		    ValueError: If the movie update fails.
		"""
		update = update_movie_info(request).where(movie_info_table.columns.id == request.id)
		if update is not None:
			result = self._session.execute(update).first()
			if result:
				return to_movie_info(result[0])
			raise ValueError('Error while updating movie info')
		return self.select_movie(request.id)
