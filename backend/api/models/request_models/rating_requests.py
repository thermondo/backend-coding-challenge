from typing import Optional

from pydantic import BaseModel, Field


class CreateRatingInfoAPIRequest(BaseModel):
    rating: int = Field(
        ...,
        description='The rating given to the movie, typically on a scale of 1 to 5.',
        ge=1,
        le=5,
    )
    movie_info_id: int = Field(..., description='The unique identifier for the movie being rated.')
    review: Optional[str] = Field(
        None,
        description='An optional text review provided by the user as movie text review.',
        min_length=4,
        max_length=64,
    )

    class Config:
        json_schema_extra = {
            'example': {
                'rating': 4,
                'movie_info_id': 42,
                'review': 'An exhilarating experience with stunning visuals and a compelling storyline.',
            }
        }
