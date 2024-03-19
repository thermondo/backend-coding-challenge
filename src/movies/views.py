from flask import Blueprint, redirect, render_template, request, url_for

from src import tmdb
from src.movies.models import Movie

from .forms import MovieSearchForm


movies_bp = Blueprint("movies", __name__)


@movies_bp.route("/movies/<movie_id>", methods=["GET"])
def show(movie_id):
    movie = Movie.get_by_id(movie_id)
    if movie:
        poster_image_url = tmdb.get_poster_image_url(movie.poster_path)
        return render_template(
            "movies/show.html", movie=movie, poster_url=poster_image_url)
    else:
        return redirect(url_for("movies.search"))


@movies_bp.route("/search", methods=["GET", "POST"])
def search():
    form = MovieSearchForm(request.form)
    if form.validate_on_submit():
        # Get movie search query from form
        # Search DB for movie
        # For now, also search TMDB <- this is not what I would do for prod
        # Add TMDB results to our own DB
        # Return results from TMDB
        # Merge and sort the two results
        # Send results
        search_results_from_db = Movie.search_by_query_string(
            form.query_string.data)
        search_results_from_tmdb = Movie.search_by_query_string_tmdb(
            form.query_string.data)
        # Merge and sort the two results
        results_by_id = {m.id: m for m in search_results_from_db}
        for tmdb_res in search_results_from_tmdb:
            results_by_id[tmdb_res.id] = tmdb_res
        merged_results = list(results_by_id.values())
        # Sorted by most recent movies first
        merged_results.sort(key=lambda movie: movie.release_date, reverse=True)
        return render_template(
            "movies/search_results.html", search_results=merged_results)

    return render_template("movies/search.html", form=form)
