from typing import Generator

import pytest
from sqlalchemy import create_engine, orm

from enviroment import TEST_DATABASE_URI
from repository.tests.fixtures.test_database_setup import create_database_if_not_exists
from repository.unit_of_work import SessionFactory

# from tests.fixtures.custom_fixtures import generator_fixture, fixture, Scope


@pytest.fixture(scope='session')
def db_url() -> Generator[str, None, None]:
	if TEST_DATABASE_URI is None:
		raise ValueError('TEST_DATABASE_URI is missing from test environment')
	yield TEST_DATABASE_URI


@pytest.fixture(scope='session')
def database_session(db_url) -> orm.Session:
	create_database_if_not_exists(db_url)
	return SessionFactory(database_url=db_url, create_engine=create_engine)()
