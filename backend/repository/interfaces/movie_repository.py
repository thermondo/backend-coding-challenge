from abc import ABC
from typing import List, Optional

from domain_models.movie_info import MovieInfoModel
from repository.models import (
    CreateMovieInfoRequest,
    UpdateMovieInfoRequest,
)


class MovieInfoRepository(ABC):
    def create_movie(self, request: CreateMovieInfoRequest) -> MovieInfoModel:
        raise NotImplementedError

    def select_movies(
        self,
        query: Optional[str] = None,
        offset: int = 0,
        limit: int = 10,
    ) -> List[MovieInfoModel]:
        raise NotImplementedError

    def select_movie(self, movie_id: int) -> Optional[MovieInfoModel]:
        raise NotImplementedError

    def count_movies(self, query: Optional[str] = None) -> int:
        raise NotImplementedError

    def update_movie(self, request: UpdateMovieInfoRequest) -> Optional[MovieInfoModel]:
        raise NotImplementedError
