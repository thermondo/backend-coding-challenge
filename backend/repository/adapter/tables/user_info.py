from sqlalchemy import Boolean, Column, String, BigInteger

from repository.adapter.tables.base_table import BaseTable
from repository.adapter.tables.fields.passwordField import Password

user_info_table = BaseTable(
	'user_info',
	Column('name', String, nullable=False, unique=True),
	Column('activation_code', String),
	Column('activation_expiry_date', BigInteger),
	Column('password', Password, nullable=False),
	Column('active', Boolean, nullable=False),
)
