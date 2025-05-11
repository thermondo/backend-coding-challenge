from typing import List, Optional

from sqlalchemy import orm, and_
import pickle

from domain_models.rating_info import RatingInfoModel
from domain_models.rating_report import RatingReportModel
from enviroment import REDIS_URL
from repository.models import (
	CreateRatingInfoRequest,
	UpdateRatingInfoRequest,
)
from repository.models import (
	CreateRatingReportRequest,
	UpdateRatingReportRequest,
)
from repository.adapter.tables.rating_info import rating_info_table
from repository.adapter.tables.rating_report import rating_report_table
from repository.interfaces.rating_repository import RatingRepository
from repository.sqlalchemy_repository.rating.mappers import (
	to_rating_info,
	to_rating_report,
	to_ratings_info,
)
from repository.sqlalchemy_repository.rating.queries import (
	insert_rating_info,
	insert_rating_report_entry,
	update_rating_info,
	update_rating_report_entry,
	select_rating_info_as_json,
	select_rating_report_as_json,
	select_movie_average_rating,
)
import redis
from logger import init_logger

logger = init_logger(__name__)


class SQLAlchemyRatingRepository(RatingRepository):
	def __init__(self, session: orm.Session):
		"""
		Initializes the repository with a SQLAlchemy session and Redis client.

		Parameters:
		    session (orm.Session): SQLAlchemy session object for database interactions.

		Returns:
		    None
		"""
		self._session = session
		self.redis_client = redis.from_url(REDIS_URL)

	def create_rating_info(self, request: CreateRatingInfoRequest) -> Optional[RatingInfoModel]:
		"""
		Creates a new rating info entry or updates the existing one if it exists for the same movie and user.

		Parameters:
		    request (CreateRatingInfoRequest): The request object containing movie_info_id, user_info_id,
		                                        rating, review, and active status.

		Returns:
		    Optional[RatingInfoModel]: The created or updated RatingInfoModel object if successful.
		                               Raises ValueError if an error occurs during creation or update.
		"""
		existing_rating_info = self.select_rating_info_by_movie_and_user_id(
			movie_info_id=request.movie_info_id,
			user_info_id=request.user_info_id,
		)
		if existing_rating_info:
			return self.update_rating_info(
				UpdateRatingInfoRequest(
					id=existing_rating_info.id,
					rating=request.rating,
					review=request.review,
					active=request.active,
				)
			)
		insert = insert_rating_info(request)
		result = self._session.execute(insert).first()
		if result:
			return to_rating_info(result[0])
		raise ValueError('error while creating rating info object')

	def create_rating_report_entry(self, movie_info_id: int) -> Optional[RatingReportModel]:
		"""
		Creates or updates a rating report entry for a specific movie. This method bypasses the cache to
		ensure accurate rating aggregation, particularly when underlying ratings have changed.

		To write a new entry or update an existing one, the cache must be bypassed to ensure the latest
		average rating is captured from the database, avoiding stale data issues.

		Parameters:
		    movie_info_id (int): The ID of the movie for which the rating report is being created or updated.

		Returns:
		    Optional[RatingReportModel]: The created or updated RatingReportModel object if successful.
		                                 Raises ValueError if an error occurs during creation or update.
		"""
		average_query_result = self._session.execute(
			select_movie_average_rating(movie_info_id)
		).first()
		average = 0
		if average_query_result:
			average = average_query_result[1]
		exiting_movie_report = self.select_rating_report_for_movie(
			movie_info_id=movie_info_id, use_cache_db=False
		)
		if exiting_movie_report:
			self._invalidate_rating_report_from_cache(exiting_movie_report.id, movie_info_id)
			return self.update_rating_report_entry(
				UpdateRatingReportRequest(
					id=exiting_movie_report.id,
					accumulated_rating=average,
				)
			)
		insert = insert_rating_report_entry(
			CreateRatingReportRequest(movie_info_id=movie_info_id, accumulated_rating=average)
		)
		result = self._session.execute(insert).first()
		if result:
			return to_rating_report(result[0])
		raise ValueError('error while creating rating report entry object')

	def select_rating_info(self, rating_info_id: int) -> Optional[RatingInfoModel]:
		"""
		Retrieves a rating info record by its ID.

		Parameters:
		    rating_info_id (int): The ID of the rating info entry to retrieve.

		Returns:
		    Optional[RatingInfoModel]: The RatingInfoModel object if found, otherwise None.
		"""
		select = select_rating_info_as_json().where(rating_info_table.columns.id == rating_info_id)
		result = self._session.execute(select).first()
		if result:
			return to_rating_info(result[0])
		return None

	def select_rating_info_by_movie_and_user_id(
		self, movie_info_id: int, user_info_id: int
	) -> Optional[RatingInfoModel]:
		select = select_rating_info_as_json().where(
			and_(
				rating_info_table.columns.movie_info_id == movie_info_id,
				rating_info_table.columns.user_info_id == user_info_id,
			)
		)
		result = self._session.execute(select).first()
		if result:
			return to_rating_info(result[0])
		return None

	def _save_rating_report_in_cache(self, report: RatingReportModel):
		"""
		Saves a RatingReportModel object in the Redis cache using both the report ID and movie ID as keys.

		Parameters:
		    report (RatingReportModel): The RatingReportModel object to be cached.
		"""
		# Serialize the object
		serialized_report = pickle.dumps(report)

		self.redis_client.set(f'rating:{report.id}', serialized_report)
		self.redis_client.set(f'rating:movie:{report.movie.id}', serialized_report)

	def _get_rating_report_by_report_entry_id(
		self, report_entry_id: int
	) -> Optional[RatingReportModel]:
		"""
		Retrieves a RatingReportModel from the Redis cache using the report entry ID.

		Parameters:
		    report_entry_id (int): The ID of the report entry to retrieve from the cache.

		Returns:
		    RatingReportModel: The RatingReportModel object if found in the cache, otherwise None.
		"""
		serialized_report = self.redis_client.get(f'rating:{report_entry_id}')
		if serialized_report:
			logger.info(
				f'cache hit: reading RatingReportModel with report_entry_id {report_entry_id} from cache'
			)
			return pickle.loads(serialized_report)
		return None

	def _get_rating_report_by_movie_info_id(
		self, movie_info_id: int
	) -> Optional[RatingReportModel]:
		"""
		Retrieves a RatingReportModel from the Redis cache using the movie info ID.

		Parameters:
		    movie_info_id (int): The ID of the movie to retrieve the rating report for.

		Returns:
		    RatingReportModel: The RatingReportModel object if found in the cache, otherwise None.
		"""
		serialized_report = self.redis_client.get(f'rating:movie:{movie_info_id}')
		if serialized_report:
			print(
				f'cache hit: reading RatingReportModel with movie_info_id {movie_info_id} from cache'
			)
			return pickle.loads(serialized_report)
		return None

	def _invalidate_rating_report_from_cache(
		self, report_entry_id: int, movie_info_id: int
	) -> None:
		"""
		Invalidates (removes) a cached RatingReportModel from Redis by its report entry ID and movie info ID.

		Parameters:
		    report_entry_id (int): The ID of the rating report entry to remove from the cache.
		    movie_info_id (int): The ID of the movie associated with the rating report entry.
		"""
		self.redis_client.delete(f'rating:{report_entry_id}')
		self.redis_client.delete(f'rating:movie:{movie_info_id}')
		logger.info(
			f'Invalidated RatingReportModel with ID {report_entry_id} and Movie ID {movie_info_id} from cache'
		)

	def select_rating_report_entry(self, rating_report_id: int) -> Optional[RatingReportModel]:
		"""
		Retrieves a rating report entry by its ID, using the Redis cache for faster access if possible.

		Parameters:
		    rating_report_id (int): The ID of the rating report entry to retrieve.

		Returns:
		    RatingReportModel: The rating report model if found, otherwise None.
		"""
		result_from_cache = self._get_rating_report_by_report_entry_id(rating_report_id)
		if result_from_cache:
			return result_from_cache
		select = select_rating_report_as_json().where(
			rating_report_table.columns.id == rating_report_id
		)
		result = self._session.execute(select).first()
		if result:
			rating_report = to_rating_report(result[0])
			self._save_rating_report_in_cache(rating_report)
			return rating_report
		return None

	def select_rating_info_for_user(
		self,
		user_info_id: int,
		offset: int = 0,
		limit: int = 10,
	) -> List[RatingInfoModel]:
		"""
		Retrieves a list of rating info records for a specific user, with support for pagination.

		Parameters:
		    user_info_id (int): The ID of the user to filter the ratings.
		    offset (int): The number of records to skip (default is 0).
		    limit (int): The maximum number of records to return (default is 10).

		Returns:
		    List[RatingInfoModel]: A list of RatingInfoModel objects.
		"""
		select = (
			select_rating_info_as_json()
			.where(rating_info_table.columns.user_info_id == user_info_id)
			.limit(limit)
			.offset(offset)
			.order_by(rating_info_table.columns.date_created.asc())
		)
		result = self._session.execute(select)
		return to_ratings_info(result)

	def select_rating_report_for_movie(
		self, movie_info_id: int, use_cache_db: bool = True
	) -> Optional[RatingReportModel]:
		"""
		Retrieves the rating report for a specified movie, with optional caching.

		Parameters:
		    movie_info_id (int): The ID of the movie to retrieve the rating report for.
		    use_cache_db (bool): Whether to attempt to retrieve the report from the cache before querying the database. Defaults to True.

		Returns:
		    Optional[RatingReportModel]: The rating report model if found, otherwise None.
		"""
		result_from_cache = self._get_rating_report_by_movie_info_id(movie_info_id)
		if result_from_cache and use_cache_db:
			return result_from_cache
		select = select_rating_report_as_json().where(
			rating_report_table.columns.movie_info_id == movie_info_id
		)
		result = self._session.execute(select).first()
		if result:
			rating_report = to_rating_report(result[0])
			self._save_rating_report_in_cache(rating_report)
			return rating_report

	def update_rating_info(self, request: UpdateRatingInfoRequest) -> Optional[RatingInfoModel]:
		"""
		Updates the rating info for a specified movie.

		Parameters:
		    request (UpdateRatingInfoRequest): The update object for the target rating info.

		Returns:
		    Optional[RatingInfoModel]: The updated rating info model if found, otherwise None.
		"""
		update = update_rating_info(request).where(rating_info_table.columns.id == request.id)
		if update is not None:
			result = self._session.execute(update).first()
			if result:
				return to_rating_info(result[0])
			raise ValueError('error while updating rating info')
		return self.select_rating_info(request.id)

	def update_rating_report_entry(
		self, request: UpdateRatingReportRequest
	) -> Optional[RatingReportModel]:
		"""
		Updates the rating report entry for a specified movie.

		Parameters:
		    request (UpdateRatingReportRequest): The update object for the target rating report entry .

		Returns:
		    Optional[RatingReportModel]: The updated rating report entry  model if found, otherwise None.
		"""
		update = update_rating_report_entry(request).where(
			rating_report_table.columns.id == request.id
		)
		if update is not None:
			result = self._session.execute(update).first()
			if result:
				return to_rating_report(result[0])
			raise ValueError('error while updating rating report')
		return self.select_rating_report_entry(request.id)
