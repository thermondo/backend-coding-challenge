import os
import random
import string
from typing import Optional

from sqlalchemy import LargeBinary, Text, TypeDecorator
from sqlalchemy.dialects.postgresql import BYTEA

from domain_models.user_info import PasswordHash


class Password(TypeDecorator):
	"""Allows storing and retrieving password hashes using PasswordHash."""

	cache_ok = False
	impl = Text

	def __init__(self, salt: Optional[str] = None, **kwds):
		super(Password, self).__init__(**kwds)
		if not salt:
			salt = ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(22))
		self.salt = salt

	def process_bind_param(self, value, dialect) -> str:
		"""Ensure the value is a PasswordHash and then return its hash."""
		if value:
			converted_hash_value = self._convert(value)
			return converted_hash_value.hash if converted_hash_value else ''
		return ''

	def process_result_value(self, value, dialect) -> Optional[PasswordHash]:
		"""Convert the hash to a PasswordHash, if it's non-NULL."""
		if value is not None:
			return PasswordHash(value)
		return None

	def validator(self, password) -> Optional[PasswordHash]:
		"""Provides a validator/converter for @validates usage."""
		return self._convert(password)

	def _convert(self, value) -> Optional[PasswordHash]:
		"""Returns a PasswordHash from the given string.

		PasswordHash instances or None values will return unchanged.
		Strings will be hashed and the resulting PasswordHash returned.
		Any other input will result in a TypeError.
		"""
		if isinstance(value, PasswordHash):
			return value
		elif isinstance(value, str):
			return PasswordHash.new(value)
		elif value is not None:
			raise TypeError('Cannot convert {} to a PasswordHash'.format(type(value)))
		return None
