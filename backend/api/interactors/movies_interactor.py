from typing import List, Optional, Dict

from api.models.response_models.movie_info_response import (
	MovieInfoResponse,
	MoviesInfoResponse,
)

from domain_models.movie_info import MovieInfoModel


class MoviesInfoInteractor:
	"""
	Interactor class that handles the transformation of movie information models into response models.

	This class provides methods to convert individual movie information and lists of movie information
	into response models that can be returned from the API. It also supports the inclusion of movie ratings.
	"""

	def __init__(self) -> None:
		pass

	@staticmethod
	def to_movie_info_response(
		movie_info: MovieInfoModel, rating: Optional[int] = None
	) -> MovieInfoResponse:
		"""
		Converts a single movie information model to a movie info response model.

		This method takes a `MovieInfoModel` and an optional rating and returns a corresponding
		`MovieInfoResponse` object. If a rating is provided, it will be included in the response.

		Args:
		    movie_info (MovieInfoModel): The movie information model to convert.
		    rating (Optional[int]): The movie's rating, if available (default is None).

		Returns:
		    MovieInfoResponse: The converted movie information response.
		"""
		return MovieInfoResponse(
			id=movie_info.id,
			title=movie_info.title,
			description=movie_info.description or '',
			release_year=movie_info.release_year or '',
			rating=rating,
		)

	def to_movies_info_response(
		self,
		movies_info: List[MovieInfoModel],
		movies_rating: Dict[str, int],
		count: int = 0,
	) -> MoviesInfoResponse:
		"""
		Converts a list of movie information models to a movies info response model.

		This method takes a list of `MovieInfoModel` objects and their corresponding ratings
		(in a dictionary), and returns a `MoviesInfoResponse` containing the movie information
		along with their ratings. It also includes the total count of movies.

		Args:
		    movies_info (List[MovieInfoModel]): A list of movie information models to convert.
		    movies_rating (Dict[str, int]): A dictionary mapping movie IDs to their ratings.
		    count (int): The total number of movies (default is 0).

		Returns:
		    MoviesInfoResponse: The converted list of movie information responses.
		"""
		return MoviesInfoResponse(
			movies=[
				self.to_movie_info_response(
					movie_info,
					movies_rating[str(movie_info.id)]
					if movies_rating[str(movie_info.id)]
					else None,
				)
				for movie_info in movies_info
			],
			total_count=count,
		)
