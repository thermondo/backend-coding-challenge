from dataclasses import dataclass
from datetime import datetime
from typing import Optional

from passlib.context import CryptContext

from domain_models.base_model import BaseDomainModel

pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')


class PasswordHash(object):
    def __init__(self, hashed_password: str):
        self._hash = hashed_password

    def __eq__(self, candidate: object):
        """Hashes the candidate string and compares it to the stored hash."""
        return pwd_context.verify(candidate, self._hash)

    def __repr__(self):
        """Simple object representation."""
        return '<{}>'.format(type(self).__name__)

    @classmethod
    def new(cls, plain_password: str):
        """Creates a PasswordHash from the given password."""
        return cls(pwd_context.hash(plain_password))

    @property
    def hash(self):
        return self._hash


@dataclass
class UserInfoModel(BaseDomainModel):
    name: str
    active: bool
    hashed_password: PasswordHash
    activation_code: Optional[str]
    activation_expiry_date: Optional[datetime]

    def __init__(
        self,
        id: int,
        name: str,
        hashed_password: PasswordHash,
        active: bool = True,
        activation_code: Optional[str] = None,
        activation_expiry_date: Optional[datetime] = None,
        date_created: Optional[datetime] = None,
        date_updated: Optional[datetime] = None,
    ):
        super().__init__(id=id, date_created=date_created, date_updated=date_updated)
        self.name = name
        self.active = active
        self.hashed_password = hashed_password
        self.activation_code = activation_code
        self.activation_expiry_date = activation_expiry_date
