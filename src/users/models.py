from typing import List

from flask_login import UserMixin
from sqlalchemy import select
from sqlalchemy.orm import Mapped, relationship

from src import bcrypt, db


class User(UserMixin, db.Model):

    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, unique=True, nullable=False)
    email = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=db.func.now())
    ratings: Mapped[List["Rating"]] = relationship(  # noqa: F821
        back_populates='user', lazy='select')

    def __init__(self, username: str, password: str, email: str = ''):
        self.username = username
        self.email = email
        self.password = bcrypt.generate_password_hash(password)

    def __repr__(self):
        return f"<username {self.username} email {self.email}>"

    @classmethod
    def get_by_username(cls, username: str):
        result = db.session.scalars(
            select(cls).where(cls.username == username)
        ).one_or_none()
        return result
