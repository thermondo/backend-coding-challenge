from typing import Generator
from urllib.parse import urlparse

import pytest
from sqlalchemy import orm, text
from tenacity import retry, retry_if_not_exception_type, stop_after_attempt, wait_fixed
from sqlalchemy import create_engine

from enviroment import DEFAULT_DATABASE_URI, TEST_DATABASE_URI
from repository.adapter import meta_data
from repository.tests.fixtures.clear_database import CLEAR_DATABASE
import psycopg2

persistent = retry(
	wait=wait_fixed(1),
	stop=stop_after_attempt(5),
	reraise=True,
	retry=retry_if_not_exception_type(FileNotFoundError),
)


@pytest.fixture(autouse=True)
def database_setup(database_session) -> Generator:
	session = database_session
	wipe_session(session)
	yield
	wipe_session(session)
	session.close()


# TODO: Create test database if it is not exists (must be refactored and placed only once per test session)
def create_database_if_not_exists(TEST_DATABASE_URI_INPUT):
	parsed_url = urlparse(TEST_DATABASE_URI_INPUT)
	username = parsed_url.username
	password = parsed_url.password
	host = parsed_url.hostname
	port = parsed_url.port
	db_name = parsed_url.path[1:]
	connection_string = (
		f'dbname=postgres user={username} password={password} host={host} port={port}'
	)

	try:
		conn = psycopg2.connect(connection_string)
		conn.autocommit = True
		cursor = conn.cursor()

		# Check if the database exists
		cursor.execute(f"SELECT 1 FROM pg_database WHERE datname = '{db_name}'")
		exists = cursor.fetchone()

		if not exists:
			# Create the database if it doesn't exist
			cursor.execute(f'CREATE DATABASE {db_name}')
			print(f"Database '{db_name}' created successfully.")
		else:
			print(f"Database '{db_name}' already exists.")

		cursor.close()

	except Exception as e:
		print(f'Error checking or creating database: {e}')
	finally:
		if conn:
			conn.close()


def wipe_session(session: orm.Session) -> None:
	drop_tables_and_views(session)
	create_tables_and_views(session)


def create_tables_and_views(session: orm.Session) -> None:
	engine = session.get_bind()
	persistent(meta_data.create_all)(engine)
	session.commit()


def drop_tables_and_views(session: orm.Session) -> None:
	session.execute(text(CLEAR_DATABASE))
	session.commit()
