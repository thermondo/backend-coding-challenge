"""
Base Sqlalchemy Table Module.
"""

from typing import Any

from sqlalchemy import BigInteger, Column, Integer, Table

from repository.adapter import meta_data
from utils import make_timestamp


class BaseTable:
	def __init__(self, name: str, *args, **kwargs) -> None:  # noqa: ANN002, ANN003
		self._table = Table(
			name,
			meta_data,
			Column('id', Integer, primary_key=True, autoincrement=True),
			Column('date_created', BigInteger, default=make_timestamp),
			Column(
				'date_updated',
				BigInteger,
				default=make_timestamp,
				onupdate=make_timestamp,
			),
			*args,
			**kwargs,
		)

	def alias(self, _alias: str) -> 'BaseTable':
		self._table.alias(_alias)
		return self

	@property
	def name(self) -> str:
		return self._table.name

	@property
	def table(self) -> Table:
		return self._table

	@property
	def columns(self) -> Any:
		return self._table.columns

	def has_column(self, column: str) -> bool:
		return column in [column.key for column in self.columns]
