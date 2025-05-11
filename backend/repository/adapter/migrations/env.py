import logging
from logging.config import fileConfig

from alembic import context
from sqlalchemy import engine_from_config, pool

from enviroment import DATABASE_URI
from repository.adapter import meta_data
from repository.adapter.tables import user_info, movie_info, rating_info, rating_report

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.

config = context.config

# Interpret the config file for Python logging.
# This line sets up loggers basically.
if config.config_file_name is None:
	raise TypeError('The config file name is not set')
fileConfig(config.config_file_name)
logger = logging.getLogger('alembic.env')


if not config.attributes.get('is_test'):
	config.set_main_option('sqlalchemy.url', DATABASE_URI)
target_metadata = meta_data


def run_migrations_offline() -> None:
	"""
	Run migrations in 'offline' mode.

	This configures the context with just a URL
	and not an Engine, though an Engine is acceptable
	here as well.  By skipping the Engine creation
	we don't even need a DBAPI to be available.

	Calls to context.execute() here emit the given string to the
	script output.
	"""
	url = config.get_main_option('sqlalchemy.url')
	context.configure(
		url=url,
		target_metadata=target_metadata,
		literal_binds=True,
		dialect_opts={'paramstyle': 'named'},
		render_as_batch=True,
		compare_type=True,
	)

	with context.begin_transaction():
		context.run_migrations()


def run_migrations_online() -> None:
	"""
	Run migrations in 'online' mode.

	In this scenario we need to create an Engine and associate a
	connection with the context.
	"""
	connectable = engine_from_config(
		config.get_section(config.config_ini_section) or {},
		prefix='sqlalchemy.',
		poolclass=pool.NullPool,
	)

	with connectable.connect() as connection:
		context.configure(
			connection=connection,
			target_metadata=target_metadata,
			render_as_batch=True,
			compare_type=True,
		)

		with context.begin_transaction():
			context.run_migrations()


if context.is_offline_mode():
	run_migrations_offline()
else:
	run_migrations_online()
