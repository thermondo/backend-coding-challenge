from abc import ABC
from typing import List, Optional

from domain_models.user_info import UserInfoModel
from repository.models import (
	CreateUserInfoRequest,
	UpdateUserInfoRequest,
)


class UserInfoRepository(ABC):
	def create_user(self, request: CreateUserInfoRequest) -> UserInfoModel:
		raise NotImplementedError

	def select_users(self) -> List[UserInfoModel]:
		raise NotImplementedError

	def select_user(self, user_id: int) -> Optional[UserInfoModel]:
		raise NotImplementedError

	def select_user_by_name(self, name: str) -> Optional[UserInfoModel]:
		raise NotImplementedError

	def update_user(self, request: UpdateUserInfoRequest) -> Optional[UserInfoModel]:
		raise NotImplementedError
