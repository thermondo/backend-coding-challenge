from typing import Any, Optional, Type

from pydantic import BaseModel
from sqlalchemy import TypeDecorator
from sqlalchemy.dialects.postgresql.json import JSONB


class PydanticField(TypeDecorator):
	impl = JSONB
	cache_ok = False
	model_type: Type[BaseModel]

	def __init__(self, model_type: Type[BaseModel]):
		super().__init__()
		self.model_type = model_type

	def process_bind_param(self, value: Optional[BaseModel], dialect: Any) -> dict:
		if value:
			return value.dict()
		return {}

	def process_result_value(self, value: Optional[dict], dialect: Any) -> BaseModel:
		return self.model_type(**value if value else {})

	# def process_literal_param(self, value: Any, dialect: Any) -> str:
	#     return value
