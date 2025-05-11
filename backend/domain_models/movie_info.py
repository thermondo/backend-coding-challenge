from dataclasses import dataclass
from datetime import datetime
from typing import Optional
from domain_models.base_model import BaseDomainModel


@dataclass
class MovieInfoModel(BaseDomainModel):
    title: str
    active: bool
    release_year: Optional[str]
    description: Optional[str]

    def __init__(
        self,
        id: int,
        title: str,
        active: bool = True,
        release_year: Optional[str] = None,
        description: Optional[str] = None,
        date_created: Optional[datetime] = None,
        date_updated: Optional[datetime] = None,
    ):
        super().__init__(id=id, date_created=date_created, date_updated=date_updated)
        self.title = title
        self.active = active
        self.release_year = release_year
        self.description = description
