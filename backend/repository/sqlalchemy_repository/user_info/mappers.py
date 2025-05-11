from typing import Any, Dict

from domain_models.user_info import PasswordHash, UserInfoModel
from utils import from_timestamp


def to_user_info(payload: Dict[str, Any]) -> UserInfoModel:
    return UserInfoModel(
        name=payload['name'],
        id=payload['id'],
        hashed_password=PasswordHash(payload['hashed_password']),
        activation_code=payload['activation_code'],
        activation_expiry_date=from_timestamp(payload['activation_expiry_date'])
        if payload['activation_expiry_date']
        else None,
        date_created=from_timestamp(payload['date_created']),
        date_updated=from_timestamp(payload['date_updated']),
        active=payload['active'],
    )
