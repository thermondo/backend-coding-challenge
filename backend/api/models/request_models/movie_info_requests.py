from typing import Optional

from pydantic import BaseModel, Field


class CreateMovieAPIRequest(BaseModel):
	title: str = Field(
		...,
		description='The title of the movie, typically a unique identifier for the film.',
	)
	release_year: Optional[str] = Field(
		None,
		description='The year the movie was released, usually in YYYY format. Optional field.',
	)
	description: Optional[str] = Field(
		None,
		description="A brief summary or overview of the movie's plot. Optional field.",
	)

	class Config:
		json_schema_extra = {
			'example': {
				'title': 'Dark night',
				'release_year': '2019',
				'description': 'A skilled thief is given a chance to erase his criminal record by performing an impossible task.',
			}
		}
