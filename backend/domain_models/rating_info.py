from dataclasses import dataclass
from datetime import datetime
from typing import Optional
from domain_models.base_model import BaseDomainModel
from domain_models.movie_info import MovieInfoModel
from domain_models.user_info import UserInfoModel


@dataclass
class RatingInfoModel(BaseDomainModel):
	user: UserInfoModel
	movie: MovieInfoModel
	rating: int
	review: Optional[str]
	active: bool

	def __init__(
		self,
		id: int,
		user: UserInfoModel,
		movie: MovieInfoModel,
		rating: int,
		review: Optional[str] = None,
		active: bool = True,
		date_created: Optional[datetime] = None,
		date_updated: Optional[datetime] = None,
	):
		super().__init__(id=id, date_created=date_created, date_updated=date_updated)
		self.user = user
		self.active = active
		self.movie = movie
		self.rating = rating
		self.review = review
