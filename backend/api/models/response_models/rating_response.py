from enum import Enum
from typing import Optional, List, Dict

from pydantic import BaseModel

from api.models.response_models.base_response import BaseResponseModel
from api.models.response_models.movie_info_response import MovieInfoResponse
from api.models.response_models.user_info_response import UserResponse


class RatingInfoResponse(BaseResponseModel):
    id: int
    rating: int
    movie_info: Dict
    review: Optional[str] = None
    user_info: Optional[Dict] = None


class RatingReportResponse(BaseResponseModel):
    id: int
    rating: int
    movie_info: Dict


class RatingsInfoResponse(BaseResponseModel):
    ratings: List[RatingInfoResponse]
    total_count: int = 0
