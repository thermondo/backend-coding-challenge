from injector import Injector, singleton
from sqlalchemy import create_engine
from enviroment import DATABASE_URI
from repository.unit_of_work import (
    RepositoriesFactory,
    SessionFactory,
    SQLAlchemyUnitOfWork,
)


def assemble(injector: Injector) -> None:
    injector.binder.bind(RepositoriesFactory, to=RepositoriesFactory)

    def make_session_factory() -> SessionFactory:
        return SessionFactory(database_url=DATABASE_URI, create_engine=create_engine)

    injector.binder.bind(SessionFactory, to=make_session_factory)

    injector.binder.bind(
        SQLAlchemyUnitOfWork,
        to=lambda: SQLAlchemyUnitOfWork(
            session_factory=injector.get(SessionFactory),
            repositories_factory=injector.get(RepositoriesFactory),
        ),
        scope=singleton,
    )
