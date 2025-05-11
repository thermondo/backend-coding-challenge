from datetime import datetime
from dataclasses import dataclass
from typing import Optional


@dataclass
class CreateUserInfoRequest:
	name: str
	password: str
	active: bool = True
	activation_code: Optional[str] = None
	activation_expiry_date: Optional[int] = None


@dataclass
class UpdateUserInfoRequest:
	id: int
	active: bool
	password: Optional[str] = None
	activation_code: Optional[str] = None
	activation_expiry_date: Optional[int] = None
