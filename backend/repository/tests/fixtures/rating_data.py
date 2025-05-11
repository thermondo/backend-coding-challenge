from api.models.response_models.user_info_response import UserResponse
from domain_models.movie_info import MovieInfoModel
from domain_models.user_info import UserInfoModel, PasswordHash
from repository.adapter.tables.movie_info import movie_info_table
from time import time

from repository.adapter.tables.user_info import user_info_table
from utils import from_timestamp


def add_movies_test_data(insert_rows, number_of_movies: int = 1):
    time_stamp = int(time() * 1000)
    db_rows = []
    domain_models = []
    for index in range(number_of_movies):
        db_rows.append(
            {
                'title': f'name_{index}',
                'description': 'description',
                'date_created': time_stamp,
                'date_updated': time_stamp,
                'active': True,
                'id': index + 1,
            }
        )
        domain_models.append(
            MovieInfoModel(
                title=f'name_{index}',
                active=True,
                description='description',
                date_created=from_timestamp(time_stamp),
                date_updated=from_timestamp(time_stamp),
                id=index + 1,
            )
        )
    insert_rows(db_rows, movie_info_table.table)
    return domain_models


def add_users_test_data(insert_rows, number_of_users: int = 1):
    time_stamp = int(time() * 1000)
    db_rows = []
    domain_models = []
    for index in range(number_of_users):
        db_rows.append(
            {
                'name': f'name_{index}',
                'password': '6767676',
                'date_created': time_stamp,
                'date_updated': time_stamp,
                'active': True,
                'id': index + 1,
            },
        )
        domain_models.append(
            UserInfoModel(
                name=f'name_{index}',
                active=True,
                hashed_password=PasswordHash('hashed_password'),
                date_created=from_timestamp(time_stamp),
                date_updated=from_timestamp(time_stamp),
                id=1,
            )
        )
    insert_rows(db_rows, user_info_table.table)
    return domain_models
