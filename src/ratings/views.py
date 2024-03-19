from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import login_required

from src import db
from src.users.models import User
from src.ratings.models import Rating

from .forms import RatingForm


ratings_bp = Blueprint("ratings", __name__)


@ratings_bp.route("/new-rating", methods=["GET", "POST"])
@login_required
def new_rating():
    form = RatingForm(request.form)
    if form.validate_on_submit():
        user_id = User.get_by_username(form.username.data).id
        rating = Rating(
            movie_id=form.movie_id.data,
            user_id=user_id,
            value=form.rating_value.data,
            review=form.review.data)
        db.session.add(rating)
        db.session.commit()

        flash("Thanks for adding your rating!", "success")

        return redirect(url_for("core.home"))

    return render_template("ratings/add_rating.html", form=form)
