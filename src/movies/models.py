from datetime import datetime

from sqlalchemy import select

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

    def __init__(
            self,
            title: str,
            release_date: str,
            tmdb_id: int = 0,
            poster_path: str = '',
            overview: str = ''):
        self.tmdb_id = tmdb_id
        self.title = title
        self.release_date = release_date
        self.poster_path = poster_path
        self.overview = overview

    def __repr__(self):
        return (f"<id {self.id} tmdb_id {self.tmdb_id} title {self.title} "
                f"release_date {self.release_date}>")

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
                )
                db.session.add(new_movie_obj)
                db_objects.append(new_movie_obj)
        # Save new objects
        db.session.commit()
        return db_objects
