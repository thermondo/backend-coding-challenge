from typing import Optional, List

from fastapi import APIRouter, Depends, Response
from injector import Injector
from typing_extensions import Annotated

from api.interactors.movies_interactor import MoviesInfoInteractor
from api.models.request_models.movie_info_requests import CreateMovieAPIRequest
from api.models.response_models.base_response import ResponseModel
from api.interactors.user_interactor import (
	UserInfoInteractor,
	oauth2_scheme,
)
from api.enpoints.interfaces import EndPoint
from api.models.response_models.error_response import ErrorResponse
from domain_models.movie_info import MovieInfoModel

from repository.models import CreateMovieInfoRequest
from repository.unit_of_work import Repositories, SQLAlchemyUnitOfWork
from logger import init_logger

logger = init_logger(__name__)


class MovieEndPoint(EndPoint):
	def __init__(self, injector: Injector) -> None:
		"""Initialize the Movie EndPoint with the required dependencies."""
		super().__init__()
		self._unit_of_work = injector.get(SQLAlchemyUnitOfWork)
		self._user_interactor = injector.get(UserInfoInteractor)
		self._movies_interactor = injector.get(MoviesInfoInteractor)

	async def get_movies(
		self,
		token: Annotated[str, Depends(oauth2_scheme)],
		query: str = None,
		offset: int = 0,
		limit: int = 10,
	) -> Response:
		"""Fetch a list of movies with optional filters for query, offset, and limit.

		Parameters:
		    token (str): User authorization token.
		    query (str, optional): Search query to filter movies, can be used to filter movies by title or description.
		    offset (int, optional): The starting index for pagination.
		    limit (int, optional): The pagination maximum number of records.

		Returns:
		    ResponseModel: A response containing the list of movies according to the filter options.
		"""
		try:
			# Check if the token is still valid
			if self._user_interactor.is_valid_user(token):
				# 1- get the movies records from db
				def select_movie_transaction(
					repositories: Repositories,
				) -> List[MovieInfoModel]:
					return repositories.movie_info.select_movies(
						query=query, offset=offset, limit=limit
					)

				movies = self._unit_of_work.perform(select_movie_transaction)

				# 2- get the total count of all records matching the query to be used by the pagination functionalities
				def count_transaction(repositories: Repositories) -> int:
					return repositories.movie_info.count_movies(query=query)

				count = self._unit_of_work.perform(count_transaction)

				# 3- get the rating for the listed movies
				def rating_transaction(repositories: Repositories, **kwargs) -> int:
					movie_info_id_args: Optional[str] = kwargs.get('movie_info_id', None)
					movie_info_id: Optional[int] = (
						int(movie_info_id_args) if movie_info_id_args else None
					)
					if movie_info_id:
						movie_report_entry = repositories.rating.select_rating_report_for_movie(
							movie_info_id=movie_info_id
						)
						return movie_report_entry.accumulated_rating if movie_report_entry else 0
					return 0

				movies_rating = {
					str(movie_info_id): self._unit_of_work.perform(
						rating_transaction, movie_info_id=movie_info_id
					)
					for movie_info_id in [movie.id for movie in movies]
				}

				# 4- process the response
				return ResponseModel(
					self._movies_interactor.to_movies_info_response(movies, movies_rating, count)
				)

		except Exception as err:
			logger.error(f'request token: {token}, msg: {str(err)}')
			return ResponseModel(
				ErrorResponse(
					error='Error while getting movies info.',
					status_code=500,
				)
			)
		return ResponseModel(ErrorResponse(error='unknown error', status_code=401))

	async def get_movie(
		self,
		token: Annotated[str, Depends(oauth2_scheme)],
		movie_id: int,
	) -> Response:
		"""Fetch detailed information about a specific movie by its ID.

		Parameters:
		    token (str): User authorization token.
		    movie_id (int): The unique identifier of the movie.

		Returns:
		    ResponseModel: A response containing the movie details and rating.
		"""
		try:
			if self._user_interactor.is_valid_user(token):
				# 1- get the movie record
				def transaction(repositories: Repositories) -> Optional[MovieInfoModel]:
					return repositories.movie_info.select_movie(
						movie_id=movie_id,
					)

				movie = self._unit_of_work.perform(transaction)

				# abort if no movie found
				if not movie:
					return ResponseModel(ErrorResponse(status_code=404, error='Movie not found'))

				# 2- get the related rating
				def rating_transaction(repositories: Repositories) -> int:
					movie_report_entry = repositories.rating.select_rating_report_for_movie(
						movie_info_id=movie_id
					)
					return movie_report_entry.accumulated_rating if movie_report_entry else 0

				movie_rating = self._unit_of_work.perform(rating_transaction)

				return ResponseModel(
					self._movies_interactor.to_movie_info_response(movie, movie_rating)
				)

		except Exception as err:
			logger.error(f'request token: {token}, msg: {str(err)}')
			return ResponseModel(
				ErrorResponse(
					error='Error while getting movie info.',
					status_code=500,
				)
			)
		return ResponseModel(ErrorResponse(error='unknown error', status_code=401))

	async def create_movie(
		self,
		token: Annotated[str, Depends(oauth2_scheme)],
		movie_info_request: CreateMovieAPIRequest,
	) -> Response:
		"""Create a new movie record in the database.

		Parameters:
		    token (str): User authorization token.
		    movie_info_request (CreateMovieAPIRequest): The movie details to create.

		Returns:
		    ResponseModel: A response containing the created movie details.
		"""
		try:
			if self._user_interactor.is_valid_user(token):

				def transaction(repositories: Repositories) -> Optional[MovieInfoModel]:
					return repositories.movie_info.create_movie(
						CreateMovieInfoRequest(
							title=movie_info_request.title,
							release_year=movie_info_request.release_year,
							description=movie_info_request.description,
						)
					)

				created_movie = self._unit_of_work.perform(transaction)

				return ResponseModel(
					self._movies_interactor.to_movie_info_response(created_movie, 0)
				)
		except Exception as err:
			logger.error(f'request token: {token}, msg: {str(err)}')
			return ResponseModel(
				ErrorResponse(
					error='Error while creating movie record.',
					status_code=500,
				)
			)
		return ResponseModel(ErrorResponse(error='unknown error', status_code=401))

	def router(self) -> APIRouter:
		"""Setup the API routes for the Movie endpoints."""
		router = APIRouter(
			prefix='/movie',
			tags=['Movies'],
		)
		router.add_api_route(
			'/',
			self.get_movies,
			methods=['GET'],
			summary='Get Movies',
			description='Fetch a list of movies with optional filters for pagination and search.',
		)
		router.add_api_route(
			'/',
			self.create_movie,
			methods=['POST'],
			summary='Create Movie',
			description='Create a new movie record.',
		)
		router.add_api_route(
			'/{movie_id}',
			self.get_movie,
			methods=['GET'],
			summary='Get Movie',
			description='Fetch detailed information about a specific movie by its ID.',
		)
		return router
