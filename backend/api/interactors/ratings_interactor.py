from typing import List

from api.interactors.user_interactor import UserInfoInteractor
from api.interactors.movies_interactor import MoviesInfoInteractor
from api.models.response_models.movie_info_response import MoviesInfoResponse
from api.models.response_models.rating_response import (
	RatingInfoResponse,
	RatingReportResponse,
	RatingsInfoResponse,
)

from domain_models.rating_info import RatingInfoModel
from domain_models.rating_report import RatingReportModel


class RatingsInfoInteractor:
	"""
	Interactor class that handles the transformation of rating information models into response models.

	This class provides methods to convert individual rating information, rating reports, and lists of ratings
	into response models that can be returned from the API. It also supports the transformation of user-related
	ratings and rating reports with or without user information.

	Attributes:
	    _movies_utils (MoviesInfoInteractor): The movies interactor used for converting movie information.
	    _user_utils (UserInfoInteractor): The user interactor used for converting user information.
	"""

	def __init__(
		self,
		movies_interactor: MoviesInfoInteractor,
		user_interactor: UserInfoInteractor,
	) -> None:
		self._movies_utils = movies_interactor
		self._user_utils = user_interactor

	def to_rating_info_response(
		self,
		rating_info: RatingInfoModel,
		display_user_info: bool = True,
	) -> RatingInfoResponse:
		"""
		Converts a single rating information model into a rating info response model.

		This method takes a `RatingInfoModel` and optionally includes user information in the response.
		If `display_user_info` is `True`, it will include the user details; otherwise, it will exclude them.

		Args:
		    rating_info (RatingInfoModel): The rating information model to convert.
		    display_user_info (bool): Whether to include the user information in the response (default is True).

		Returns:
		    RatingInfoResponse: The converted rating information response.
		"""
		return RatingInfoResponse(
			id=rating_info.id,
			movie_info=self._movies_utils.to_movie_info_response(rating_info.movie).dict(),
			user_info=self._user_utils.to_user_response(rating_info.user).dict()
			if display_user_info
			else None,
			rating=rating_info.rating,
			review=rating_info.review,
		)

	def to_rating_report_response(
		self,
		rating_report: RatingReportModel,
	) -> RatingReportResponse:
		"""
		Converts a single rating report model into a rating report response model.

		This method takes a `RatingReportModel` and returns a corresponding `RatingReportResponse` model,
		including the movie information and accumulated rating.

		Args:
		    rating_report (RatingReportModel): The rating report model to convert.

		Returns:
		    RatingReportResponse: The converted rating report response.
		"""
		return RatingReportResponse(
			id=rating_report.id,
			movie_info=self._movies_utils.to_movie_info_response(rating_report.movie).dict(),
			rating=rating_report.accumulated_rating,
		)

	def to_ratings_info_response(
		self, ratings_info: List[RatingInfoModel], count: int = 0
	) -> RatingsInfoResponse:
		"""
		Converts a list of rating information models into a ratings info response model.

		This method takes a list of `RatingInfoModel` objects and returns a `RatingsInfoResponse` containing
		the rating information and the total count of ratings.

		Args:
		    ratings_info (List[RatingInfoModel]): A list of rating information models to convert.
		    count (int): The total number of ratings (default is 0).

		Returns:
		    RatingsInfoResponse: The converted list of rating information responses.
		"""
		return RatingsInfoResponse(
			ratings=[self.to_rating_info_response(rating_info) for rating_info in ratings_info],
			total_count=count,
		)

	def to_user_related_ratings_info_response(
		self, ratings_info: List[RatingInfoModel], count: int = 0
	) -> RatingsInfoResponse:
		"""
		Converts a list of user-related rating information models into a ratings info response model, excluding
		user information.

		This method is similar to `to_ratings_info_response`, but it excludes the user information from the response.

		Args:
		    ratings_info (List[RatingInfoModel]): A list of rating information models to convert.
		    count (int): The total number of ratings (default is 0).

		Returns:
		    RatingsInfoResponse: The converted list of user-related rating information responses without user data.
		"""
		return RatingsInfoResponse(
			ratings=[
				self.to_rating_info_response(
					rating_info,
					display_user_info=False,
				)
				for rating_info in ratings_info
			],
			total_count=count,
		)
