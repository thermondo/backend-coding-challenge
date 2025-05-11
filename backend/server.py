"""
Setup server and activate api routes.
"""

from typing import Any, Optional

import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from injector import Injector

from api.enpoints.movie.movie_endpoints import MovieEndPoint
from api.enpoints.rating.rating_endpoints import RatingEndPoint
from api.enpoints.user.user_endpoints import UserInfoEndPoint
from core_injector import make_injector
from domain_models.user_info import UserInfoModel
from dummy_data import MoviesData
from logger import init_logger
from repository.models import CreateUserInfoRequest
from repository.unit_of_work import Repositories, SQLAlchemyUnitOfWork


def create_test_user_if_not_exists() -> None:
    def select_transaction(repositories: Repositories) -> Optional[UserInfoModel]:
        return repositories.user_info.select_user_by_name('test@test.de')

    user_info = fast_app_injector.get(SQLAlchemyUnitOfWork).perform(select_transaction)
    if not user_info:

        def create_user_transaction(
            repositories: Repositories,
        ) -> Optional[UserInfoModel]:
            return repositories.user_info.create_user(
                CreateUserInfoRequest(name='test@test.de', password='test', active=True)
            )

        fast_app_injector.get(SQLAlchemyUnitOfWork).perform(create_user_transaction)


def create_dummy_movies():
    def transaction(repositories: Repositories) -> None:
        for i in range(len(MoviesData)):
            movie_in_db = repositories.movie_info.select_movie(i + 1)
            if not movie_in_db:
                repositories.movie_info.create_movie(MoviesData[i])

    fast_app_injector.get(SQLAlchemyUnitOfWork).perform(transaction)


origins = [
    'http://localhost',
    'http://localhost:3000',
]

LOG = init_logger(__name__)

allowed_headers = [
    'Access-Control-Request-Headers',
    'Access-Control-Request-Method',
    'Authorization',
    'Content-Type',
    'Host',
    'User-Agent',
    'Accept',
    'Accept-Language',
    'Accept-Encoding',
    'X-Fields',
    'Content-Length',
    'Origin',
    'Connection',
    'Referer',
]

API_PREFIX = '/api'
HOST = '0.0.0.0'  # noqa: S104
PORT = 50050
RELOAD = True


fast_app_injector = make_injector()


def create_app(app_injector: Injector) -> FastAPI:
    user_end_point = UserInfoEndPoint(app_injector)
    movie_end_point = MovieEndPoint(app_injector)
    rating_end_point = RatingEndPoint(app_injector)
    app = FastAPI()

    # app.include_router(ae_end_point.router(), prefix=API_PREFIX)
    app.include_router(user_end_point.router(), prefix=API_PREFIX)
    app.include_router(movie_end_point.router(), prefix=API_PREFIX)
    app.include_router(rating_end_point.router(), prefix=API_PREFIX)
    app.add_middleware(
        CORSMiddleware,
        allow_origins=['*'],
        allow_credentials=True,
        allow_methods=['*'],
        allow_headers=['*'],
    )

    async def http_exception_handler(_: Any, exc: HTTPException) -> JSONResponse:
        return JSONResponse(
            status_code=exc.status_code,
            content=exc.detail,
        )

    app.add_exception_handler(HTTPException, http_exception_handler)
    return app


def start_app() -> None:
    """
    Start aidkit API.

    Activate all routes.
    """

    LOG.info(
        'Starting server on %s:%i with arguments: RELOAD=%s',
        HOST,
        PORT,
        RELOAD,
    )

    uvicorn.run(
        app='server:APP',
        host=HOST,
        port=PORT,
        reload=RELOAD,
    )


APP = create_app(fast_app_injector)
create_test_user_if_not_exists()
create_dummy_movies()

if __name__ == '__main__':
    start_app()
