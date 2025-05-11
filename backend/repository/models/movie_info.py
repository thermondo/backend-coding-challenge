from datetime import datetime
from dataclasses import dataclass
from typing import Optional


@dataclass
class CreateMovieInfoRequest:
	title: str
	active: bool = True
	release_year: Optional[str] = None
	description: Optional[str] = None


@dataclass
class UpdateMovieInfoRequest:
	id: int
	active: Optional[bool] = None
	title: Optional[str] = None
	release_year: Optional[str] = None
	description: Optional[int] = None
