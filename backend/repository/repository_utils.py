import re
from typing import Any, Dict, List, Optional, Union

from sqlalchemy import (
	Column,
	func,
	insert,
	select,
	update,
)

from sqlalchemy.sql.dml import Insert, Update
from sqlalchemy.sql import Select, Subquery
from sqlalchemy.sql import label

from repository.adapter.tables.abanos_table import BaseTable


def update_table_rows(table: BaseTable, values: Dict[str, Any]) -> update:
	return update(table.table).values(values)


def insert_into_table(table: BaseTable, values: List[Dict[str, Any]]) -> insert:
	return insert(table.table).values(values)


def select_from(
	table: Union[BaseTable, Select],
	columns: List[Union[Column, func, label]],
) -> Select:
	if isinstance(table, BaseTable):
		return select().select_from(table.table).with_only_columns(*tuple(columns))
	return select().select_from(table).with_only_columns(*tuple(columns))  # type: ignore


def select_from_table_as_json(
	select_from: Union[BaseTable, Subquery],
	object_columns: Dict[str, Union[Column, Select, Subquery]],
	aggregate_result: bool = False,
	json_object_alias: Optional[str] = None,
) -> Select:
	if isinstance(select_from, Subquery):
		return (
			select()
			.select_from(select_from)
			.with_only_columns(
				*tuple([json_column(object_columns, aggregate_result, json_object_alias)])
			)
		)
	return (
		select()
		.select_from(select_from.table)
		.with_only_columns(
			*tuple([json_column(object_columns, aggregate_result, json_object_alias)])
		)
	)


def csv_value_to_list(value: Optional[str] = None) -> List[str]:
	if not value:
		return []
	spliced_value = re.split(r'(?<!\\),', value)
	return [s.replace('\\,', ',') for s in spliced_value]


def list_to_csv_value(value: Optional[List[str]] = None) -> Optional[str]:
	if not value or len(value) == 0:
		return None
	return ','.join([s.replace(',', '\\,') for s in value])


def json_column(
	json_object: Dict[str, Union[Column, Select, Subquery]],
	aggregate_result: bool = False,
	alias: str = 'json_object',
):
	def _resolve_json_object_column() -> func:
		items = json_object.items()
		json_build_object_column = func.json_build_object(
			*tuple(
				element
				for cols_tuple in tuple(
					(
						key,
						value,
					)
					for key, value in items
				)
				for element in cols_tuple
			)
		)
		if aggregate_result:
			return func.json_agg(json_build_object_column)
		return json_build_object_column

	return _resolve_json_object_column().label(alias)
