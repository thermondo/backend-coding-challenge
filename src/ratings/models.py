from sqlalchemy import select
from sqlalchemy import UniqueConstraint

from sqlalchemy.orm import Mapped, relationship

from src import db


class Rating(db.Model):
    __table_args__ = (UniqueConstraint('movie_id', 'user_id'), )
    __tablename__ = "ratings"

    id = db.Column(db.Integer, primary_key=True)
    movie_id = db.Column(db.Integer, db.ForeignKey("movies.id"), index=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), index=True)
    value = db.Column(db.Integer)
    review = db.Column(db.Text)
    created_at = db.Column(
        db.DateTime,
        nullable=False,
        default=db.func.now())
    movie: Mapped["Movie"] = relationship(  # noqa: F821
        back_populates='ratings', lazy='select')
    user: Mapped["User"] = relationship(  # noqa: F821
        back_populates='ratings', lazy='select')

    def __init__(
            self,
            movie_id: int,
            user_id: int,
            value: int,
            review: str = ''
            ):
        self.movie_id = movie_id
        self.user_id = user_id
        self.value = value
        self.review = review

    def __repr__(self):
        return (f"<id {self.id} movie_id {self.tmdb_id} user_id {self.title} "
                f"value {self.release_date}>")

    @classmethod
    def create_and_save(
            cls, movie_id: int, user_id: int, value: int, review: str = ''):
        new_rating = cls(movie_id, user_id, value, review)
        db.session.add(new_rating)
        db.session.commit()
        return new_rating

    @classmethod
    def get_all_by_movie(cls, movie_id):
        results = db.session.scalars(
            select(cls).where(cls.movie_id == movie_id).order_by(
                cls.created_at.desc())
        ).all()
        return results

    @classmethod
    def get_all_by_user(cls, user_id):
        results = db.session.scalars(
            select(cls).where(cls.user_id == user_id).order_by(
                cls.created_at.desc())
        ).all()
        return results
