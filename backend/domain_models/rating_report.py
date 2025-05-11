from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal
from typing import Optional
from domain_models.base_model import BaseDomainModel
from domain_models.movie_info import MovieInfoModel
from domain_models.user_info import UserInfoModel


@dataclass
class RatingReportModel(BaseDomainModel):
    movie: MovieInfoModel
    accumulated_rating: Decimal

    def __init__(
        self,
        id: int,
        movie: MovieInfoModel,
        accumulated_rating: Decimal,
        date_created: Optional[datetime] = None,
        date_updated: Optional[datetime] = None,
    ):
        super().__init__(id=id, date_created=date_created, date_updated=date_updated)
        self.accumulated_rating = accumulated_rating
        self.movie = movie
