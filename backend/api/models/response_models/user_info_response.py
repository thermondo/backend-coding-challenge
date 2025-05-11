from enum import Enum
from typing import Optional

from pydantic import BaseModel

from api.models.response_models.base_response import BaseResponseModel


class UserResponse(BaseResponseModel):
	username: str
	email: Optional[str] = None
	full_name: Optional[str] = None
	active: Optional[bool] = None


class Token(BaseModel):
	access_token: str
	token_type: str


class TokenData(BaseModel):
	username: Optional[str] = None


class SignUpStatus(str, Enum):
	FAILED = 'FAILED'
	ALREADY_EXISTS = 'ALREADY_EXISTS'
	SUCCEED = 'SUCCEED'


class SignUpResponse(BaseResponseModel):
	user: Optional[UserResponse] = None
	message: Optional[str] = None
	status: str


class ActivateAccountResponse(BaseResponseModel):
	user: Optional[UserResponse] = None
	message: Optional[str] = None
	isActivated: bool


class ChangePasswordResponse(BaseResponseModel):
	user: Optional[UserResponse] = None
	message: Optional[str] = None
	isChanged: bool
