from typing import Any, Dict, Optional

from sqlalchemy import Insert, Select, Update

from repository.models import (
    CreateUserInfoRequest,
    UpdateUserInfoRequest,
)
from repository.adapter.tables.user_info import user_info_table
from repository.repository_utils import (
    insert_into_table,
    json_column,
    select_from_table_as_json,
    update_table_rows,
)


def user_info_column_as_dict() -> Dict:
    return {
        'id': user_info_table.table.columns.id,
        'name': user_info_table.table.columns.name,
        'active': user_info_table.table.columns.active,
        'hashed_password': user_info_table.table.columns.password,
        'activation_code': user_info_table.table.columns.activation_code,
        'activation_expiry_date': user_info_table.table.columns.activation_expiry_date,
        'date_created': user_info_table.table.columns.date_created,
        'date_updated': user_info_table.table.columns.date_updated,
    }


def select_user_info_as_json() -> Select:
    return select_from_table_as_json(user_info_table, user_info_column_as_dict())


def insert_user_info(request: CreateUserInfoRequest) -> Insert:
    return insert_into_table(
        user_info_table,
        [
            {
                'name': request.name,
                'active': request.active,
                'password': request.password,
                'activation_code': request.activation_code,
                'activation_expiry_date': request.activation_expiry_date,
            }
        ],
    ).returning(json_column(user_info_column_as_dict()))


def update_user_info(request: UpdateUserInfoRequest) -> Optional[Update]:
    update_obj: Dict[str, Any] = {}

    if request.active is not None:
        update_obj['active'] = request.active
    if request.activation_code is not None:
        update_obj['activation_code'] = request.activation_code
    if request.activation_expiry_date is not None:
        update_obj['activation_expiry_date'] = request.activation_expiry_date
    if request.password is not None:
        update_obj['password'] = request.password

    if update_obj:
        return update_table_rows(user_info_table, update_obj).returning(
            json_column(user_info_column_as_dict())
        )
    return None
