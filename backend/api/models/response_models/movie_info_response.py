from decimal import Decimal
from enum import Enum
from typing import Optional, List, Union

from pydantic import BaseModel

from api.models.response_models.base_response import BaseResponseModel


class MovieInfoResponse(BaseResponseModel):
	id: int
	title: str
	rating: Optional[Union[float, Decimal]] = None
	released_year: Optional[str] = None
	description: Optional[str] = None


class MoviesInfoResponse(BaseResponseModel):
	movies: List[MovieInfoResponse]
	total_count: int = 0
