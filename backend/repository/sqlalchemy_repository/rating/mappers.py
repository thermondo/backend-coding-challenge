from decimal import Decimal
from typing import Any, Dict, List

from sqlalchemy import Result

from domain_models.rating_info import RatingInfoModel
from domain_models.rating_report import RatingReportModel
from repository.sqlalchemy_repository.movie_info.mappers import to_movie_info
from repository.sqlalchemy_repository.user_info.mappers import to_user_info
from utils import from_timestamp


def to_rating_info(payload: Dict[str, Any]) -> RatingInfoModel:
    if not payload['movie_info'] or not payload['user_info']:
        raise ValueError('Rating info deserialize error: no movie or user info')
    movie_info = to_movie_info(payload['movie_info'])
    user_info = to_user_info(payload['user_info'])
    return RatingInfoModel(
        id=payload['id'],
        movie=movie_info,
        user=user_info,
        rating=payload['rating'],
        review=payload['review'],
        date_created=from_timestamp(payload['date_created']),
        date_updated=from_timestamp(payload['date_updated']),
        active=payload['active'],
    )


def to_rating_report(payload: Dict[str, Any]) -> RatingReportModel:
    if not payload['movie_info']:
        raise ValueError('Rating report deserialize error: no movie info')
    movie_info = to_movie_info(payload['movie_info'])
    return RatingReportModel(
        id=payload['id'],
        movie=movie_info,
        accumulated_rating=payload['accumulated_rating'],
        date_created=from_timestamp(payload['date_created']),
        date_updated=from_timestamp(payload['date_updated']),
    )


def to_ratings_info(result: Result) -> List[RatingInfoModel]:
    selected_rows: List[RatingInfoModel] = []
    for row in result:
        selected_rows.append(to_rating_info(row[0]))
    return selected_rows


def to_ratings_report(result: Result) -> List[RatingReportModel]:
    selected_rows: List[RatingReportModel] = []
    for row in result:
        selected_rows.append(to_rating_report(row[0]))
    return selected_rows
