from sqlalchemy import Column, Integer, ForeignKey, Numeric

from repository.adapter.tables.abanos_table import BaseTable
from repository.adapter.tables.movie_info import movie_info_table

rating_report_table = BaseTable(
	'rating_report',
	Column(
		'movie_info_id',
		Integer,
		ForeignKey(movie_info_table.columns.id, ondelete='CASCADE'),
		nullable=False,
	),
	Column('accumulated_rating', Numeric(precision=10, scale=2)),
)
