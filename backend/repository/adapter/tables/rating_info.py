from sqlalchemy import Boolean, Column, String, ForeignKey, Integer

from repository.adapter.tables.base_table import BaseTable
from repository.adapter.tables.movie_info import movie_info_table
from repository.adapter.tables.user_info import user_info_table

rating_info_table = BaseTable(
	'rating_info',
	Column(
		'movie_info_id',
		Integer,
		ForeignKey(movie_info_table.columns.id, ondelete='CASCADE'),
		nullable=False,
	),
	Column(
		'user_info_id',
		Integer,
		ForeignKey(user_info_table.columns.id, ondelete='CASCADE'),
		nullable=False,
	),
	Column('review', String),
	Column('rating', Integer),
	Column('active', Boolean, nullable=False, default=True),
)
