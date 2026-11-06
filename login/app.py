import os
import re
import sqlite3
from functools import wraps
from pathlib import Path

import click
from flask import (
    Flask,
    flash,
    redirect,
    render_template,
    request,
    session,
    url_for,
)
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_wtf.csrf import CSRFProtect
from werkzeug.security import check_password_hash, generate_password_hash


BASE_DIR = Path(__file__).resolve().parent
DATABASE = BASE_DIR / "users.db"

app = Flask(
    __name__,
    template_folder="../templates",
    static_folder="../static"
)
secret_key = os.environ.get("FLASK_SECRET_KEY")

if not secret_key:
    raise RuntimeError(
        "Set FLASK_SECRET_KEY before starting the application."
    )

app.config.update(
    SECRET_KEY=secret_key,
    SESSION_COOKIE_HTTPONLY=True,
    SESSION_COOKIE_SECURE=os.environ.get("COOKIE_SECURE", "0") == "1",
    SESSION_COOKIE_SAMESITE="Lax",
    PERMANENT_SESSION_LIFETIME=1800,
    MAX_CONTENT_LENGTH=16 * 1024,
)

csrf = CSRFProtect(app)

limiter = Limiter(
    get_remote_address,
    app=app,
    default_limits=[],
    storage_uri=os.environ.get("RATELIMIT_STORAGE_URI", "memory://"),
)


def get_db():
    connection = sqlite3.connect(DATABASE)
    connection.row_factory = sqlite3.Row
    return connection


def init_db():
    with get_db() as db:
        db.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL COLLATE NOCASE UNIQUE,
                password_hash TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)


init_db()


def login_required(function):
    @wraps(function)
    def wrapper(*args, **kwargs):
        if "user_id" not in session:
            return redirect(url_for("login"))

        return function(*args, **kwargs)

    return wrapper


@app.after_request
def security_headers(response):
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
    response.headers["Cache-Control"] = "no-store"

    return response


@app.route("/", methods=["GET", "POST"])
@limiter.limit("5 per minute", methods=["POST"])
def login():

    if "user_id" in session:
        return redirect(url_for("welcome"))

    if request.method == "POST":

        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")

        if (
            not username
            or not password
            or len(username) > 80
            or len(password) > 1024
        ):
            flash("Invalid username or password.", "error")
            return render_template("login.html"), 400

        with get_db() as db:
            user = db.execute(
                """
                SELECT id, username, password_hash
                FROM users
                WHERE username = ?
                """,
                (username,),
            ).fetchone()

        if user and check_password_hash(
            user["password_hash"], password
        ):
            session.clear()

            session["user_id"] = user["id"]
            session["username"] = user["username"]
            session.permanent = True

            return redirect(url_for("welcome"))

        flash("Invalid username or password.", "error")

    return render_template("login.html")


@app.route("/welcome")
@login_required
def welcome():

    return render_template(
        "welcome.html",
        username=session["username"]
    )


@app.route("/logout", methods=["POST"])
@login_required
def logout():

    session.clear()

    flash("You have successfully logged out.", "success")

    return redirect(url_for("login"))


@app.cli.command("create-user")
def create_user():

    """Create a user account from the terminal."""

    username = click.prompt("Username").strip()

    if not re.fullmatch(r"[A-Za-z0-9_.-]{3,80}", username):
        raise click.ClickException(
            "Username must be 3-80 characters and use letters, "
            "numbers, dots, underscores or hyphens."
        )

    password = click.prompt(
        "Password",
        hide_input=True,
        confirmation_prompt=True
    )

    if len(password) < 12 or len(password) > 1024:
        raise click.ClickException(
            "Password must be between 12 and 1024 characters."
        )

    password_hash = generate_password_hash(
        password,
        method="scrypt"
    )

    try:
        with get_db() as db:
            db.execute(
                """
                INSERT INTO users (username, password_hash)
                VALUES (?, ?)
                """,
                (username, password_hash)
            )

        click.echo("Account created successfully.")

    except sqlite3.IntegrityError:
        raise click.ClickException("Username already exists.")


if __name__ == "__main__":
    app.run(debug=False)