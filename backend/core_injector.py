from logging import Logger
from typing import Optional

from injector import Injector

from api.interactors.user_interactor import UserInfoInteractor
from api.interactors.movies_interactor import MoviesInfoInteractor
from api.interactors.ratings_interactor import RatingsInfoInteractor
from repository.assembly import assemble as assemble_repositories


def make_injector(logger: Optional[Logger] = None) -> Injector:
    injector = Injector()
    assemble_repositories(injector)

    if logger:
        injector.binder.bind(Logger, to=logger)

    user_interactor = UserInfoInteractor(injector)
    movies_interactor = MoviesInfoInteractor()
    injector.binder.bind(UserInfoInteractor, to=user_interactor)
    injector.binder.bind(MoviesInfoInteractor, to=movies_interactor)
    injector.binder.bind(
        RatingsInfoInteractor,
        to=RatingsInfoInteractor(movies_interactor, user_interactor),
    )
    return injector
