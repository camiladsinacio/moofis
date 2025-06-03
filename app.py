import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required
import requests

OMDB_API_KEY = "ac04e984"

# Configure application
app = Flask(__name__)

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///project.db")


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/", methods=["GET", "POST"])
@login_required
def index():
    types = ["movie", "show"] #define internamente evitando manipulacao pelo browser

    if request.method == "POST":
        title = request.form.get("title")
        imdb_id = request.form.get("imdb_id")
        type_ = request.form.get("type")

        if not title or not type_:
            return apology("title and type required!")

        if type_ not in types:
            return apology("invalid type!")

        user_id = session["user_id"]

        try:
            db.execute("INSERT INTO entries (user_id, title, imdb_id, type) VALUES (?, ?, ?, ?)", user_id, title, imdb_id, type_)
            flash(f"{type_.capitalize()} added successfully!", "success")
        except:
            return apology("movie or show already exists")

        return redirect("/")

    else:
        return render_template("index.html", types=types)



@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute(
            "SELECT * FROM users WHERE username = ?", request.form.get("username")
        )

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(
            rows[0]["hash"], request.form.get("password")
        ):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")

@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")

@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")

        # check for missing fields
        if not username or not password or not confirmation:
            return apology("type username and password")

        # check if passwords match
        if password != confirmation:
            return apology("passwords don't match")

        # hash the password
        hash = generate_password_hash(password)

        # try to insert user to the database
        try:
            db.execute("INSERT INTO users (username, hash) VALUES (?, ?)", username, hash)
        except:
            return apology("username already exists")

        return redirect("/login")

    else:
        return render_template("register.html")

@app.route("/delete_account", methods=["GET", "POST"])
@login_required
def delete_account():
    """deletes account"""
    user_id = session["user_id"]

    if request.method == "POST":
        # delete users transactions first
        db.execute("DELETE FROM entries WHERE user_id = ?", user_id)

        # delete user from users table
        db.execute("DELETE FROM users WHERE id = ?", user_id)

        # Clear session
        session.clear()

        flash("Account deleted successfully.")
        return redirect("/login")

    return render_template("delete_account.html")

@app.route("/movies")
@login_required
def movies():
    user_id = session["user_id"]

    movies = db.execute("SELECT * FROM entries WHERE user_id = ? AND type = 'movie' AND (status IS NULL OR status != 'watched') ORDER BY id DESC", user_id)

    # busca dados na Api para mostrar cada filme
    for movie in movies:
        imdb_id = movie.get("imdb_id")
        if imdb_id:
            response = requests.get(f"http://www.omdbapi.com/?i={imdb_id}&apikey={OMDB_API_KEY}")
            if response.status_code == 200:
                data = response.json()
                movie["plot"] = data.get("Plot", "N/A")
                movie["poster"] = data.get("Poster", None)
                movie["year"] = data.get("Year", "Unknown")
                movie["genre"] = data.get("Genre", "N/A")
                movie["director"] = data.get("Director", "N/A")
                movie["actors"] = data.get("Actors", "N/A")
                movie["imdb_rating"] = data.get("imdbRating", "N/A")
            else:
                movie["plot"] = "Plot not available."
                movie["poster"] = None
                movie["year"] = "Unknown"
                movie["genre"] = "N/A"
                movie["director"] = "N/A"
                movie["actors"] = "N/A"
                movie["imdb_rating"] = "N/A"

    return render_template("movies.html", movies=movies)

@app.route("/movies/watched")
@login_required
def watched_movies():
    user_id = session["user_id"]

    movies = db.execute("SELECT * FROM entries WHERE user_id = ? AND type = 'movie' AND (status = 'watched') ORDER BY id DESC", user_id)

    return render_template("watched_movies.html", movies=movies)

@app.route("/movies/<int:movie_id>/watched", methods=["POST"])
@login_required
def mark_movie_as_watched(movie_id):
    user_id = session["user_id"]
    db.execute("UPDATE entries SET status = 'watched' WHERE id = ? AND  user_id = ?", movie_id, user_id)
    flash("Movie marked as watched!")
    return redirect("/movies")

@app.route("/movies/<int:movie_id>/delete", methods=["POST"])
@login_required
def delete_movie(movie_id):
    user_id = session["user_id"]
    db.execute("DELETE FROM entries WHERE id = ? AND  user_id = ?", movie_id, user_id)
    flash("Movie deleted successfully!")
    return redirect(request.referrer or "/movies")


@app.route("/shows")
@login_required
def shows():
    user_id = session["user_id"]

    shows = db.execute("SELECT * FROM entries WHERE user_id = ? AND type = 'show' AND (status IS NULL OR status != 'watched') ORDER BY id DESC", user_id)

    # busca dados na Api para mostrar cada filme
    for show in shows:
        imdb_id = show.get("imdb_id")
        if imdb_id:
            response = requests.get(f"http://www.omdbapi.com/?i={imdb_id}&apikey={OMDB_API_KEY}")
            if response.status_code == 200:
                data = response.json()
                show["plot"] = data.get("Plot", "N/A")
                show["poster"] = data.get("Poster", None)
                show["year"] = data.get("Year", "Unknown")
                show["genre"] = data.get("Genre", "N/A")
                show["director"] = data.get("Director", "N/A")
                show["actors"] = data.get("Actors", "N/A")
                show["imdb_rating"] = data.get("imdbRating", "N/A")
            else:
                show["plot"] = "Plot not available."
                show["poster"] = None
                show["year"] = "Unknown"
                show["genre"] = "N/A"
                show["director"] = "N/A"
                show["actors"] = "N/A"
                show["imdb_rating"] = "N/A"

    return render_template("shows.html", shows=shows)

@app.route("/shows/watched")
@login_required
def watched_shows():
    user_id = session["user_id"]

    shows = db.execute("SELECT * FROM entries WHERE user_id = ? AND type = 'show' AND (status = 'watched') ORDER BY id DESC", user_id)

    return render_template("watched_shows.html", shows=shows)

@app.route("/shows/<int:show_id>/watched", methods=["POST"])
@login_required
def mark_show_as_watched(show_id):
    user_id = session["user_id"]
    db.execute("UPDATE entries SET status = 'watched' WHERE id = ? AND  user_id = ?", show_id, user_id)
    flash("Show marked as watched!")
    return redirect("/shows")

@app.route("/shows/<int:show_id>/delete", methods=["POST"])
@login_required
def delete_show(show_id):
    user_id = session["user_id"]
    db.execute("DELETE FROM entries WHERE id = ? AND  user_id = ?", show_id, user_id)
    flash("Show deleted successfully!")
    return redirect(request.referrer or "/shows")
