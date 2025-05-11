from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class BaseDomainModel:
    id: int
    date_created: Optional[datetime]
    date_updated: Optional[datetime]

    def __init__(
        self,
        id: int,
        date_created: Optional[datetime] = None,
        date_updated: Optional[datetime] = None,
    ):
        self.id = id
        self.date_created = date_created
        self.date_updated = date_updated
