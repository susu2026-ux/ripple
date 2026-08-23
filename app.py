from flask import Flask, redirect, render_template, request, session
import sqlite3

from werkzeug.security import check_password_hash, generate_password_hash


app = Flask(__name__)
app.config["SECRET_KEY"] = "dev"

DATABASE = "ripple.db"


def get_db():
    connection = sqlite3.connect(DATABASE)
    connection.row_factory = sqlite3.Row
    return connection


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")

        if not username or not password or not confirmation:
            return "Please fill in all fields", 400

        if password != confirmation:
            return "Passwords do not match", 400

        db = get_db()

        existing_user = db.execute(
            "SELECT * FROM users WHERE username = ?",
            (username,)
        ).fetchone()

        if existing_user:
            db.close()
            return "Username already exists", 400

        password_hash = generate_password_hash(password)

        db.execute(
            "INSERT INTO users (username, hash) VALUES (?, ?)",
            (username, password_hash)
        )
        db.commit()
        db.close()

        return redirect("/login")

    return render_template("register.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        if not username or not password:
            return "Please enter your username and password", 400

        db = get_db()

        user = db.execute(
            "SELECT * FROM users WHERE username = ?",
            (username,)
        ).fetchone()

        db.close()

        if user is None or not check_password_hash(user["hash"], password):
            return "Invalid username or password", 400

        session.clear()
        session["user_id"] = user["id"]

        return redirect("/")

    return render_template("login.html")