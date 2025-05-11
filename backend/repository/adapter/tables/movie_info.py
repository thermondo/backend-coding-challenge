from psycopg2.sql import DEFAULT
from sqlalchemy import Boolean, Column, String, BigInteger

from repository.adapter.tables.abanos_table import BaseTable
from repository.adapter.tables.fields.passwordField import Password

movie_info_table = BaseTable(
	'movie_info',
	Column('title', String, nullable=False),
	Column('description', String),
	Column('release_year', BigInteger),
	Column('active', Boolean, nullable=False, default=True),
)
