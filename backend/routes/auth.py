from flask import Blueprint, render_template, request, redirect, session, flash
from werkzeug.security import generate_password_hash, check_password_hash
from models import db, User, StudentProfile

auth = Blueprint("auth", __name__)


# ----------------------------
# DEFAULT ROUTE → LOGIN PAGE
# ----------------------------
@auth.route("/")
def index():
    return render_template("login.html")


# ----------------------------
# LOGIN PAGE (GET + POST)
# ----------------------------
@auth.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")

    email = request.form.get("email")
    password = request.form.get("password")

    user = User.query.filter_by(email=email).first()

    if not user:
        flash("User not found", "error")
        return redirect("/login")

    if not check_password_hash(user.password, password):
        flash("Incorrect password", "error")
        return redirect("/login")

    # store session
    session["user_id"] = user.id
    session["role"] = user.role
    session["name"] = user.name

    # redirect to dashboards
    if user.role == "admin":
        return redirect("/admin/dashboard")

    return redirect("/student/dashboard")


# ----------------------------
# REGISTER PAGE (GET + POST)
# ----------------------------
@auth.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("register.html")

    name = request.form.get("name")
    email = request.form.get("email")
    password = request.form.get("password")
    role = request.form.get("role")  # admin or student

    # check if user already exists
    existing_user = User.query.filter_by(email=email).first()
    if existing_user:
        flash("Email already exists!", "error")
        return redirect("/register")

    hashed_password = generate_password_hash(password)

    new_user = User(
        name=name,
        email=email,
        password=hashed_password,
        role=role
    )

    db.session.add(new_user)
    db.session.commit()

    # Create student profile if role is student
    if role == "student":
        profile = StudentProfile(user_id=new_user.id)
        db.session.add(profile)
        db.session.commit()

    flash("Registration successful! Please log in.", "success")
    return redirect("/login")


# ----------------------------
# LOGOUT
# ----------------------------
@auth.route("/logout")
def logout():
    session.clear()
    return redirect("/login")
