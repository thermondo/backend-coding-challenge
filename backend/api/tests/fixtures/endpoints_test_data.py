from typing import Optional

from fastapi.testclient import TestClient
from injector import Injector
from sqlalchemy import create_engine

from api.interactors.movies_interactor import MoviesInfoInteractor
from api.interactors.ratings_interactor import RatingsInfoInteractor
from api.interactors.user_interactor import UserInfoInteractor
from core_injector import make_injector
from domain_models.movie_info import MovieInfoModel
from domain_models.rating_info import RatingInfoModel

from domain_models.user_info import UserInfoModel
from enviroment import ACCESS_TOKEN_EXPIRE_MINUTES, TEST_DATABASE_URI
from repository.models import CreateMovieInfoRequest
from repository.models import CreateRatingInfoRequest

from repository.models import CreateUserInfoRequest
from repository.unit_of_work import (
    Repositories,
    RepositoriesFactory,
    SessionFactory,
    SQLAlchemyUnitOfWork,
)
from server import create_app
from utils import make_timestamp


def test_uow() -> SQLAlchemyUnitOfWork:
    return SQLAlchemyUnitOfWork(
        session_factory=SessionFactory(TEST_DATABASE_URI, create_engine),
        repositories_factory=RepositoriesFactory(),
    )


def make_test_injector() -> Injector:
    fast_app_injector = make_injector()
    fast_app_injector.binder.bind(SQLAlchemyUnitOfWork, test_uow())
    user_interactor = UserInfoInteractor(fast_app_injector)
    movie_interactor = MoviesInfoInteractor()
    fast_app_injector.binder.bind(UserInfoInteractor, to=user_interactor)
    fast_app_injector.binder.bind(MoviesInfoInteractor, to=movie_interactor)
    fast_app_injector.binder.bind(
        RatingsInfoInteractor,
        to=RatingsInfoInteractor(movie_interactor, user_interactor),
    )
    return fast_app_injector


def fast_api_test_app() -> TestClient:
    return TestClient(create_app(make_test_injector()))


def user_authentication_header(name: str = 'test'):
    access_token_expires = ACCESS_TOKEN_EXPIRE_MINUTES * 60 * 1000
    access_token = UserInfoInteractor.create_access_token(
        data={'sub': name}, expires_delta=access_token_expires
    )
    return {'Authorization': f'Bearer {access_token}'}


def create_test_user(
    password: str = 'test',
    count: int = 1,
    activation_code: str = 'test',
    active: bool = True,
    activation_expiry_date: int = make_timestamp(),
):
    def create_user_transaction(repositories: Repositories, **kwargs) -> Optional[UserInfoModel]:
        user_name = kwargs.get('user_name', 'test')
        return repositories.user_info.create_user(
            CreateUserInfoRequest(
                name=user_name,
                password=password,
                active=active,
                activation_code=activation_code,
                activation_expiry_date=activation_expiry_date,
            )
        )

    for i in range(count):
        name = 'test' if i == 0 else f'test_{i}'
        test_uow().perform(create_user_transaction, user_name=name)


def create_test_movie(
    count: int = 1,
    active: bool = True,
):
    def create_movie_transaction(repositories: Repositories, **kwargs) -> Optional[MovieInfoModel]:
        index = kwargs.get('index', '')
        return repositories.movie_info.create_movie(
            CreateMovieInfoRequest(
                title=f'test_movie_{index}',
                description='dummy description',
                active=active,
            )
        )

    for i in range(count):
        test_uow().perform(create_movie_transaction, index=i)


def create_test_rating(
    movie_info_id: int,
    user_info_id: int,
    rating: int,
):
    def create_rating_info_transaction(
        repositories: Repositories,
    ) -> Optional[RatingInfoModel]:
        return repositories.rating.create_rating_info(
            CreateRatingInfoRequest(
                rating=rating,
                movie_info_id=movie_info_id,
                user_info_id=user_info_id,
                review='',
            )
        )

    def create_rating_report_transaction(repositories: Repositories) -> None:
        repositories.rating.create_rating_report_entry(
            movie_info_id=movie_info_id,
        )

    test_uow().perform(create_rating_info_transaction)
    test_uow().perform(create_rating_report_transaction)


class AnyDate(int):
    def __eq__(self, other):
        return True


class AnyString(str):
    def __eq__(self, other):
        return True
