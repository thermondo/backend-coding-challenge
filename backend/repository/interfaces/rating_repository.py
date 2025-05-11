from abc import ABC
from typing import List, Optional

from redis import Redis

from domain_models.rating_info import RatingInfoModel
from domain_models.rating_report import RatingReportModel
from repository.models import (
	CreateRatingInfoRequest,
	UpdateRatingInfoRequest,
)
from repository.models import (
	CreateRatingReportRequest,
	UpdateRatingReportRequest,
)


class RatingRepository(ABC):
	redis_client: Redis

	def create_rating_info(self, request: CreateRatingInfoRequest) -> Optional[RatingInfoModel]:
		raise NotImplementedError

	def create_rating_report_entry(self, movie_info_id: int) -> Optional[RatingReportModel]:
		raise NotImplementedError

	def select_rating_info(self, rating_info_id: int) -> Optional[RatingInfoModel]:
		raise NotImplementedError

	def select_rating_info_by_movie_and_user_id(
		self, movie_info_id: int, user_info_id: int
	) -> Optional[RatingInfoModel]:
		raise NotImplementedError

	def select_rating_report_entry(self, rating_report_id: int) -> Optional[RatingReportModel]:
		raise NotImplementedError

	def select_rating_info_for_user(
		self,
		user_info_id: int,
		offset: int = 0,
		limit: int = 10,
	) -> List[RatingInfoModel]:
		raise NotImplementedError

	def select_rating_report_for_movie(self, movie_info_id: int) -> Optional[RatingReportModel]:
		raise NotImplementedError

	def update_rating_info(self, request: UpdateRatingInfoRequest) -> Optional[RatingInfoModel]:
		raise NotImplementedError

	def update_rating_report_entry(
		self, request: UpdateRatingReportRequest
	) -> Optional[RatingReportModel]:
		raise NotImplementedError
