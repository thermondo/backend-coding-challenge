from datetime import datetime
from typing import List

from sqlalchemy import select
from sqlalchemy.orm import Mapped, relationship

from src import db
from src import tmdb


class Movie(db.Model):

    __tablename__ = "movies"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    release_date = db.Column(db.String)
    overview = db.Column(db.Text)
    poster_path = db.Column(db.String)
    created_at = db.Column(
        db.DateTime,
        nullable=False,
        default=db.func.now())
    updated_at = db.Column(
        db.DateTime,
        nullable=False,
        onupdate=datetime.now,
        default=db.func.now())
    # Allow TMDB ID to be nullable to allow users to add movies that they don't
    # find in our DB or through TMDB
    tmdb_id = db.Column(db.Integer, unique=True, nullable=True, index=True)
    # TODO: rating? Average rating? Cache TMDB rating stats?
    ratings: Mapped[List["Rating"]] = relationship(  # noqa: F821
        back_populates='movie', lazy='select')
    # Let us sort by average rating and number of ratings
    tmdb_vote_average = db.Column(db.Float)
    tmdb_vote_count = db.Column(db.Integer)

    def __init__(
            self,
            title: str,
            release_date: str,
            tmdb_id: int = 0,
            poster_path: str = '',
            overview: str = '',
            tmdb_vote_average: int = 0,
            tmdb_vote_count: int = 0,
            ):
        self.tmdb_id = tmdb_id
        self.title = title
        self.release_date = release_date
        self.poster_path = poster_path
        self.overview = overview
        self.tmdb_vote_average = tmdb_vote_average
        self.tmdb_vote_count = tmdb_vote_count

    def __repr__(self):
        return (f"<id {self.id} tmdb_id {self.tmdb_id} title {self.title} "
                f"release_date {self.release_date}>")

    @classmethod
    def get_by_id(cls, movie_id):
        return db.session.get(cls, movie_id)

    @classmethod
    def get_by_tmdb_id(cls, tmdb_id):
        stmt = select(cls).where(cls.tmdb_id == tmdb_id)
        return db.session.scalars(stmt).one_or_none()

    @classmethod
    def create_and_save(
            cls,
            title: str,
            release_date: str,
            tmdb_id: int = 0,
            overview: str = ''):
        tmdb_id = tmdb_id or None
        tmdb_data = {}
        if tmdb_id:
            tmdb_data = tmdb.movie_details(tmdb_id)
        if tmdb_data:
            # Use TMDB data, not user data
            new_movie = cls(
                title=tmdb_data['title'],
                release_date=tmdb_data['release_date'],
                tmdb_id=tmdb_data['id'],
                poster_path=tmdb_data['poster_path'],
                overview=tmdb_data['overview'],
                tmdb_vote_average=tmdb_data['vote_average'],
                tmdb_vote_count=tmdb_data['vote_count'],
            )
        else:
            # If there isn't a TMDB ID or the TMDB ID didn't return data
            new_movie = cls(
                title=title,
                release_date=release_date,
                tmdb_id=tmdb_id,
                overview=overview)
        db.session.add(new_movie)
        db.session.commit()
        return new_movie

    @classmethod
    def search_by_query_string(cls, query_string):
        """
        Search for movies given a query string IN OUR DB

        Right now, this only searches titles, but ideally it would search
        other attributes as well, like overview
        """
        if not query_string:
            raise ValueError("Query string cannot be empty")

        # TODO: This is not safe and could be SQL-injected
        stmt = select(Movie).where(Movie.title.like(f'%{query_string}%'))
        results = db.session.scalars(stmt).all()
        return results

    @classmethod
    def search_by_query_string_tmdb(cls, query_string):
        """
        Search for movies given a query string IN TMDB

        Right now, this only searches titles, but ideally it would search
        other attributes as well, like overview
        """
        db_objects = []
        json_results = tmdb.search_movies(query_string)
        for movie_res in json_results.get('results', []):
            db_res = db.session.scalars(
                select(cls).where(cls.tmdb_id == movie_res['id'])
            ).one_or_none()
            if db_res:
                db_objects.append(db_res)
            else:
                new_movie_obj = cls(
                    tmdb_id=movie_res['id'],
                    title=movie_res['title'],
                    release_date=movie_res['release_date'],
                    poster_path=movie_res['poster_path'],
                    overview=movie_res['overview'],
                    tmdb_vote_average=movie_res['vote_average'],
                    tmdb_vote_count=movie_res['vote_count'],
                )
                db.session.add(new_movie_obj)
                db_objects.append(new_movie_obj)
        # Save new objects
        db.session.commit()
        return db_objects
