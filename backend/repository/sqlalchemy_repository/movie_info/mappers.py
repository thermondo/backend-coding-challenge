from typing import Any, Dict, List

from sqlalchemy import Result

from domain_models.movie_info import MovieInfoModel
from utils import from_timestamp


def to_movie_info(payload: Dict[str, Any]) -> MovieInfoModel:
    return MovieInfoModel(
        title=payload['title'],
        id=payload['id'],
        description=payload['description'],
        release_year=str(payload['release_year']) if payload['release_year'] else None,
        date_created=from_timestamp(payload['date_created']),
        date_updated=from_timestamp(payload['date_updated']),
        active=payload['active'],
    )


def to_movies_info(result: Result) -> List[MovieInfoModel]:
    selected_rows: List[MovieInfoModel] = []
    for row in result:
        selected_rows.append(to_movie_info(row._asdict()))
    return selected_rows
