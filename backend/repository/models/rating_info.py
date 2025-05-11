from datetime import datetime
from dataclasses import dataclass
from typing import Optional


@dataclass
class CreateRatingInfoRequest:
    user_info_id: int
    movie_info_id: int
    rating: int
    review: Optional[str] = None
    active: bool = True


@dataclass
class UpdateRatingInfoRequest:
    id: int
    rating: int
    review: Optional[str]
    active: bool
