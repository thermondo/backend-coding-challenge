from typing import List, Optional

from sqlalchemy import orm

from domain_models.user_info import UserInfoModel
from repository.models import (
	CreateUserInfoRequest,
	UpdateUserInfoRequest,
)
from repository.adapter.tables.user_info import user_info_table
from repository.interfaces.user_repository import UserInfoRepository
from repository.sqlalchemy_repository.user_info.mappers import to_user_info
from repository.sqlalchemy_repository.user_info.queries import (
	insert_user_info,
	select_user_info_as_json,
	update_user_info,
)


class SQLAlchemyUserInfoRepository(UserInfoRepository):
	def __init__(self, session: orm.Session):
		self._session = session

	def create_user(self, request: CreateUserInfoRequest) -> UserInfoModel:
		insert = insert_user_info(request)
		result = self._session.execute(insert).first()
		if result:
			return to_user_info(result[0])
		raise ValueError('error while creating user info object')

	def select_users(self) -> List[UserInfoModel]:
		select = select_user_info_as_json()
		result = self._session.execute(select)
		if result:
			return [to_user_info(row[0]) for row in result]
		return []

	def select_user(self, user_id: int) -> Optional[UserInfoModel]:
		select = select_user_info_as_json().where(user_info_table.columns.id == user_id)
		result = self._session.execute(select).first()
		if result:
			return to_user_info(result[0])
		return None

	def select_user_by_name(self, name: str) -> Optional[UserInfoModel]:
		select = select_user_info_as_json().where(user_info_table.columns.name == name)
		result = self._session.execute(select).first()
		if result:
			return to_user_info(result[0])
		return None

	def update_user(self, request: UpdateUserInfoRequest) -> Optional[UserInfoModel]:
		update = update_user_info(request).where(user_info_table.columns.id == request.id)
		if update is not None:
			result = self._session.execute(update).first()
			if result:
				return to_user_info(result[0])
			raise ValueError('error while updating user info')
		return self.select_user(request.id)
