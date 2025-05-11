from typing import Optional

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
		"""
		Initialize the repository with a SQLAlchemy session.

		Parameters:
		    session (orm.Session): SQLAlchemy session object for database interactions.
		"""
		self._session = session

	def create_user(self, request: CreateUserInfoRequest) -> UserInfoModel:
		"""
		Create a new user entry in the database.

		Parameters:
		    request (CreateUserInfoRequest): The request object containing user details.

		Returns:
		    UserInfoModel: The created UserInfoModel object.

		Raises:
		    ValueError: If the user creation fails.
		"""
		insert_stmt = insert_user_info(request)
		result = self._session.execute(insert_stmt).first()
		if result:
			return to_user_info(result[0])
		raise ValueError('Error while creating user info object')

	def select_user(self, user_id: int) -> Optional[UserInfoModel]:
		"""
		Retrieve a specific user record by its ID.

		Parameters:
		    user_id (int): The ID of the user to retrieve.

		Returns:
		    Optional[UserInfoModel]: The UserInfoModel object if found, otherwise None.
		"""
		select_stmt = select_user_info_as_json().where(user_info_table.columns.id == user_id)
		result = self._session.execute(select_stmt).first()
		if result:
			return to_user_info(result[0])
		return None

	def update_user(self, request: UpdateUserInfoRequest) -> Optional[UserInfoModel]:
		"""
		Update an existing user entry in the database.

		Parameters:
		    request (UpdateUserInfoRequest): The update object containing user details to be updated.

		Returns:
		    Optional[UserInfoModel]: The updated UserInfoModel object if successful, otherwise None.

		Raises:
		    ValueError: If the user update fails.
		"""
		update_stmt = update_user_info(request).where(user_info_table.columns.id == request.id)
		if update_stmt is not None:
			result = self._session.execute(update_stmt).first()
			if result:
				return to_user_info(result[0])
			raise ValueError('Error while updating user info')
		return self.select_user(request.id)
