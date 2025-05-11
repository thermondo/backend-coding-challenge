from dataclasses import dataclass
from typing import Callable, Optional, TypeVar

from sqlalchemy import orm, Engine, create_engine
from sqlalchemy.exc import SQLAlchemyError

from enviroment import DATABASE_URI
from repository.interfaces.movie_repository import MovieInfoRepository
from repository.interfaces.rating_repository import RatingRepository
from repository.interfaces.user_repository import UserInfoRepository
from repository.sqlalchemy_repository.movie_info.movie_info_repository import (
	SQLAlchemyMovieInfoRepository,
)
from repository.sqlalchemy_repository.rating.rating_repository import (
	SQLAlchemyRatingRepository,
)
from repository.sqlalchemy_repository.user_info.user_info_repository import (
	SQLAlchemyUserInfoRepository,
)
from pathlib import Path
from urllib.parse import urlparse
from alembic.config import Config
from alembic import command


@dataclass
class Repositories:
	user_info: UserInfoRepository
	movie_info: MovieInfoRepository
	rating: RatingRepository


T = TypeVar('T')
command_executed = False


class SessionFactory:
	__session_factory__: Optional[Callable[[], orm.Session]]

	def __init__(self, database_url: str, create_engine: Callable[[str], Engine]):
		session_maker = orm.sessionmaker(
			autocommit=False,
			autoflush=False,
			bind=create_engine(database_url),
		)
		self.__session_factory__ = orm.scoped_session(session_maker)

	def __call__(self, *args, **kwargs) -> orm.Session:
		if self.__session_factory__ is None:
			raise ValueError('SessionFactory.__session_factory__ is None')
		return self.__session_factory__()


class RepositoriesFactory:
	@classmethod
	def make(cls, session: orm.Session) -> Repositories:
		return Repositories(
			user_info=SQLAlchemyUserInfoRepository(session=session),
			movie_info=SQLAlchemyMovieInfoRepository(session=session),
			rating=SQLAlchemyRatingRepository(session=session),
		)


class SQLAlchemyUnitOfWork:
	_session_factory: SessionFactory

	def __init__(self, session_factory: SessionFactory, repositories_factory: RepositoriesFactory):
		self._session_factory = session_factory
		self._repositories_factory = repositories_factory
		global command_executed
		if not command_executed:
			# Execute the command
			self._create_database_if_not_exists()
			self._run_alembic_migrations()
			# Set the flag to True to prevent re-execution
			command_executed = True

	@classmethod
	def _run_alembic_migrations(cls):
		try:
			# Set up the Alembic configuration
			alembic_cfg = Config(
				str(Path(__file__).resolve().parent.parent / 'alembic.ini')
			)  # Path to your alembic.ini file
			# Run the migrations
			command.upgrade(alembic_cfg, 'head')
			print('Alembic migrations applied successfully!')
		except Exception as e:
			print(f'Error during Alembic migration: {e}')

	@classmethod
	def _create_database_if_not_exists(cls):
		# Get the default PostgreSQL URI to connect to the `postgres` database
		# Parse the connection string
		parsed_url = urlparse(DATABASE_URI)
		# Extract components
		username = parsed_url.username
		password = parsed_url.password
		host = parsed_url.hostname
		port = parsed_url.port
		db_name = parsed_url.path[1:]
		default_uri = f'postgresql://{username}:{password}@{host}:{port}/postgres'  # Use the correct credentials here
		engine = create_engine(default_uri)
		conn = engine.raw_connection()

		try:
			# Check if the database exists by querying pg_database
			with conn.cursor() as cursor:
				cursor.execute(f"SELECT 1 FROM pg_database WHERE datname='{db_name}'")
				exists = cursor.fetchone()

				if not exists:
					# Create the database if it doesn't exist
					cursor.execute(f'CREATE DATABASE {db_name}')
					conn.commit()
					print(f"Database '{db_name}' created successfully.")
				else:
					print(f"Database '{db_name}' already exists.")
		except Exception as e:
			print(f'Error checking or creating database: {e}')
		finally:
			conn.close()

	def perform(self, transaction: Callable[[Repositories], T], **kwargs) -> T:
		session = self._session_factory()
		try:
			repositories = self._repositories_factory.make(session)
			result = transaction(repositories, **kwargs)
			session.commit()
		except SQLAlchemyError as err:
			session.rollback()
			raise err
		finally:
			session.close()
		return result
