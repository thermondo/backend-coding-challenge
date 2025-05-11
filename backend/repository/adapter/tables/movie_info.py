from sqlalchemy import Boolean, Column, String, BigInteger

from repository.adapter.tables.base_table import BaseTable

movie_info_table = BaseTable(
    'movie_info',
    Column('title', String, nullable=False),
    Column('description', String),
    Column('release_year', BigInteger),
    Column('active', Boolean, nullable=False, default=True),
)
