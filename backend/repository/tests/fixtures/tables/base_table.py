from time import sleep
from typing import Any, Callable, Dict, List

import pytest
from sqlalchemy import Table, insert


@pytest.fixture
def insert_rows(database_session) -> Callable:
    def _insert_rows(rows: List[Dict[str, Any]], table: Table):
        database_session.execute(insert(table).values(rows))

    return _insert_rows
