from datetime import datetime
from time import time

from domain_models.user_info import PasswordHash, UserInfoModel
from repository.models import (
	CreateUserInfoRequest,
	UpdateUserInfoRequest,
)
from repository.adapter.tables.user_info import user_info_table
from repository.sqlalchemy_repository.user_info.user_info_repository import (
	SQLAlchemyUserInfoRepository,
)
from utils import from_timestamp


def test__when_user_info_request_is_valid_then_insert_user_info(
	database_session,
) -> None:
	model_1 = UserInfoModel(
		name='template1',
		active=True,
		hashed_password=PasswordHash('7787gsghgsgugs'),
		id=1,
	)
	repo = SQLAlchemyUserInfoRepository(database_session)
	repo.create_user(
		CreateUserInfoRequest(
			name='template1',
			password='secret',
		)
	)
	result = repo.select_user(user_id=1)

	assert result is not None
	assert result.name == model_1.name


def test__when_user_exists_then_return_valid_user_info(insert_rows, database_session) -> None:
	time_stamp = int(time() * 1000)
	rows = [
		{
			'name': 'name1',
			'password': '6767676',
			'date_created': time_stamp,
			'date_updated': time_stamp,
			'active': True,
		}
	]
	insert_rows(rows, user_info_table.table)

	repo = SQLAlchemyUserInfoRepository(database_session)
	result = repo.select_user(user_id=1)

	assert result is not None

	model_1 = UserInfoModel(
		name='name1',
		active=True,
		hashed_password=result.hashed_password,
		id=1,
		date_created=from_timestamp(time_stamp),
		date_updated=from_timestamp(time_stamp),
	)

	assert result == model_1


def test__when_user_list_is_requested_then_select_multiple_user_info(
	insert_rows, database_session
) -> None:
	time_stamp = int(time() * 1000)
	rows = [
		{
			'name': 'name1',
			'password': '6767676',
			'date_created': time_stamp,
			'date_updated': time_stamp,
			'active': True,
		},
		{
			'name': 'name2',
			'password': 'fgffdd',
			'date_created': time_stamp,
			'date_updated': time_stamp,
			'active': True,
		},
	]
	insert_rows(rows, user_info_table.table)

	repo = SQLAlchemyUserInfoRepository(database_session)
	result = repo.select_users()

	assert result is not None

	model_1 = UserInfoModel(
		name='name1',
		active=True,
		hashed_password=result[0].hashed_password,
		date_created=from_timestamp(time_stamp),
		date_updated=from_timestamp(time_stamp),
		id=1,
	)
	model_2 = UserInfoModel(
		name='name2',
		active=True,
		hashed_password=result[1].hashed_password,
		date_created=datetime.fromtimestamp(time_stamp / 1000),
		date_updated=datetime.fromtimestamp(time_stamp / 1000),
		id=2,
	)

	assert result == [model_1, model_2]


def test__when_update_is_called_with_valid_update_request_then_update_user_info(
	insert_rows, database_session
) -> None:
	rows = [{'name': 'name1', 'password': '6767676', 'active': True}]
	insert_rows(rows, user_info_table.table)
	repo = SQLAlchemyUserInfoRepository(database_session)
	repo.update_user(UpdateUserInfoRequest(id=1, active=False))
	result = repo.select_user(user_id=1)

	assert result is not None
	assert not result.active
