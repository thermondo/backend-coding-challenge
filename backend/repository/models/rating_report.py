from datetime import datetime
from dataclasses import dataclass
from decimal import Decimal
from typing import Optional


@dataclass
class CreateRatingReportRequest:
    movie_info_id: int
    accumulated_rating: Decimal


@dataclass
class UpdateRatingReportRequest:
    id: int
    accumulated_rating: Decimal
