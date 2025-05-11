from typing import Optional, List

from fastapi import APIRouter, Depends, Response, Query
from injector import Injector
from pydantic import Field
from typing_extensions import Annotated

from api.interactors.ratings_interactor import RatingsInfoInteractor
from api.models.request_models.rating_requests import CreateRatingInfoAPIRequest
from api.models.response_models.base_response import ResponseModel
from api.interactors.user_interactor import (
    UserInfoInteractor,
    oauth2_scheme,
)
from api.enpoints.interfaces import EndPoint
from api.models.response_models.error_response import ErrorResponse
from domain_models.rating_info import RatingInfoModel
from domain_models.rating_report import RatingReportModel

from repository.models import CreateRatingInfoRequest
from repository.unit_of_work import Repositories, SQLAlchemyUnitOfWork

from logger import init_logger

logger = init_logger(__name__)


class RatingEndPoint(EndPoint):
    def __init__(self, injector: Injector) -> None:
        """Initialize the Rating EndPoint with the required dependencies."""
        super().__init__()
        self._unit_of_work = injector.get(SQLAlchemyUnitOfWork)
        self._user_interactor = injector.get(UserInfoInteractor)
        self._ratings_interactor = injector.get(RatingsInfoInteractor)

    async def get_rating_for_movie(
        self,
        token: Annotated[str, Depends(oauth2_scheme)],
        movie_id: int,
    ) -> Response:
        """Fetch the rating report for a specific movie by its ID.

        Parameters:
            token (str): User authorization token.
            movie_id (int): The unique identifier of the movie.

        Returns:
            ResponseModel: A response containing the movie rating report.
        """
        try:
            if self._user_interactor.is_valid_user(token):

                def transaction(
                    repositories: Repositories,
                ) -> Optional[RatingReportModel]:
                    return repositories.rating.select_rating_report_for_movie(
                        movie_info_id=movie_id
                    )

                rating = self._unit_of_work.perform(transaction)
                return ResponseModel(self._ratings_interactor.to_rating_report_response(rating))

        except Exception as err:
            logger.error(f'request token: {token}, msg: {str(err)}')
            return ResponseModel(
                ErrorResponse(
                    error='Error while getting movie rating.',
                    status_code=500,
                )
            )
        return ResponseModel(ErrorResponse(error='unknown error', status_code=401))

    async def get_ratings_for_user(
        self,
        token: Annotated[str, Depends(oauth2_scheme)],
        offset: Annotated[
            int,
            Query(
                description='Page number of the result set',
                ge=0,
                le=1000,
            ),
        ] = 0,
        limit: Annotated[
            int,
            Query(
                description='Max number of elements per page',
                ge=0,
                le=20,
            ),
        ] = 10,
    ) -> Response:
        """Fetch all ratings given by the current user.

        Parameters:
            token (str): User authorization token.
            offset (int, optional): The starting index for pagination.
            limit (int, optional): The pagination maximum number of records.

        Returns:
            ResponseModel: A response containing the list of ratings info.
        """
        try:
            if self._user_interactor.is_valid_user(token):
                user_info = self._user_interactor.get_current_user_info(token)

                def transaction(repositories: Repositories) -> List[RatingInfoModel]:
                    return repositories.rating.select_rating_info_for_user(
                        user_info_id=user_info.id, offset=offset, limit=limit
                    )

                ratings = self._unit_of_work.perform(transaction)

                return ResponseModel(
                    self._ratings_interactor.to_user_related_ratings_info_response(ratings)
                )

        except Exception as err:
            logger.error(f'request token: {token}, msg: {str(err)}')
            return ResponseModel(
                ErrorResponse(
                    error='Error while getting ratings.',
                    status_code=500,
                )
            )
        return ResponseModel(ErrorResponse(error='unknown error', status_code=401))

    async def create_rating(
        self,
        token: Annotated[str, Depends(oauth2_scheme)],
        rating_info_request: CreateRatingInfoAPIRequest,
    ) -> Response:
        """Create a new rating for a movie.

        Parameters:
            token (str): User authorization token.
            rating_info_request (CreateRatingInfoAPIRequest): The rating details to create.

        Returns:
            ResponseModel: A response containing the created rating details.
        """
        try:
            if self._user_interactor.is_valid_user(token):
                user_info = self._user_interactor.get_current_user_info(token)

                def create_rating_info_transaction(
                    repositories: Repositories,
                ) -> Optional[RatingInfoModel]:
                    return repositories.rating.create_rating_info(
                        CreateRatingInfoRequest(
                            rating=rating_info_request.rating,
                            movie_info_id=rating_info_request.movie_info_id,
                            user_info_id=user_info.id,
                            review=rating_info_request.review,
                        )
                    )

                def create_rating_report_transaction(
                    repositories: Repositories,
                ) -> None:
                    repositories.rating.create_rating_report_entry(
                        movie_info_id=rating_info_request.movie_info_id,
                    )

                created_rating = self._unit_of_work.perform(create_rating_info_transaction)
                self._unit_of_work.perform(create_rating_report_transaction)
                return ResponseModel(
                    self._ratings_interactor.to_rating_info_response(created_rating)
                )
        except Exception as err:
            logger.error(f'request token: {token}, msg: {str(err)}')
            return ResponseModel(
                ErrorResponse(
                    error='Error while creating rating record.',
                    status_code=500,
                )
            )
        return ResponseModel(ErrorResponse(error='unknown error', status_code=401))

    def router(self) -> APIRouter:
        """Setup the API routes for the Rating endpoints."""
        router = APIRouter(
            prefix='/rating',
            tags=['Rating'],
        )
        router.add_api_route(
            '/movie/{movie_id}',
            self.get_rating_for_movie,
            methods=['GET'],
            summary='Get Movie Rating',
            description='Fetch the rating report for a specific movie by its ID.',
        )
        router.add_api_route(
            '/user',
            self.get_ratings_for_user,
            methods=['GET'],
            summary='Get User Ratings',
            description='Fetch all ratings given by the current user.',
        )
        router.add_api_route(
            '/',
            self.create_rating,
            methods=['POST'],
            summary='Create Rating',
            description='Create a new rating for a movie.',
        )
        return router
