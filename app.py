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
    if "user_id" not in session:
        return redirect("/login")

    db = get_db()
    projects = db.execute(
        "SELECT * FROM projects WHERE user_id = ?",
        (session["user_id"],)
    ).fetchall()
    db.close()

    return render_template("index.html", projects=projects)

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


@app.route("/project", methods=["GET", "POST"])
def project():
    if "user_id" not in session:
        return redirect("/login")

    if request.method == "POST":
        title = request.form.get("title")
        description = request.form.get("description")

        db = get_db()
        db.execute(
            "INSERT INTO projects (user_id, title, description) VALUES (?, ?, ?)",
            (session["user_id"], title, description)
        )
        db.commit()
        db.close()

        return redirect("/")

    return render_template("project.html")

@app.route("/project/<int:project_id>")
def project_detail(project_id):
    if "user_id" not in session:
        return redirect("/login")

    db = get_db()

    project = db.execute(
        "SELECT * FROM projects WHERE id = ? AND user_id = ?",
        (project_id, session["user_id"])
    ).fetchone()

    if project is None:
        db.close()
        return "Project not found", 404

    tasks = db.execute(
        "SELECT * FROM tasks WHERE project_id = ? ORDER BY id",
        (project_id,)
    ).fetchall()

    total_tasks = len(tasks)
    completed_tasks = sum(task["completed"] for task in tasks)

    if total_tasks > 0:
        progress = int((completed_tasks / total_tasks) * 100)
    else:
        progress = 0

    db.close()

    return render_template(
        "project_detail.html",
        project=project,
        tasks=tasks,
        progress=progress,
        completed_tasks=completed_tasks,
        total_tasks=total_tasks
    )
@app.route("/project/<int:project_id>/task", methods=["POST"])
def add_task(project_id):
    if "user_id" not in session:
        return redirect("/login")

    title = request.form.get("title")

    db = get_db()

    project = db.execute(
        "SELECT * FROM projects WHERE id = ? AND user_id = ?",
        (project_id, session["user_id"])
    ).fetchone()

    if project is None:
        db.close()
        return "Project not found", 404

    if title:
        db.execute(
            "INSERT INTO tasks (project_id, title) VALUES (?, ?)",
            (project_id, title)
        )
        db.commit()

    db.close()

    return redirect(f"/project/{project_id}")
@app.route("/task/<int:task_id>/toggle", methods=["POST"])
def toggle_task(task_id):
    if "user_id" not in session:
        return redirect("/login")

    db = get_db()

    task = db.execute(
        """
        SELECT tasks.*
        FROM tasks
        JOIN projects ON tasks.project_id = projects.id
        WHERE tasks.id = ? AND projects.user_id = ?
        """,
        (task_id, session["user_id"])
    ).fetchone()

    if task is None:
        db.close()
        return "Task not found", 404

    new_status = 0 if task["completed"] else 1

    db.execute(
        "UPDATE tasks SET completed = ? WHERE id = ?",
        (new_status, task_id)
    )
    db.commit()
    db.close()

    return redirect(f"/project/{task['project_id']}")

@app.route("/project/<int:project_id>/impact", methods=["GET", "POST"])
def impact(project_id):
    if "user_id" not in session:
        return redirect("/login")

    db = get_db()

    project = db.execute(
        "SELECT * FROM projects WHERE id = ? AND user_id = ?",
        (project_id, session["user_id"])
    ).fetchone()

    if project is None:
        db.close()
        return "Project not found", 404

    if request.method == "POST":
        volunteer_hours = request.form.get("volunteer_hours")
        people_reached = request.form.get("people_reached")

        db.execute(
            """
            INSERT INTO impact_records
            (project_id, volunteer_hours, people_reached)
            VALUES (?, ?, ?)
            """,
            (project_id, volunteer_hours, people_reached)
        )

        db.commit()
        db.close()

        return redirect(f"/project/{project_id}")

    db.close()

    return render_template(
        "impact.html",
        project=project
    )