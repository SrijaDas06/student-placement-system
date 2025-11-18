from flask import Blueprint, request, jsonify, session, render_template, redirect
from models import db, User, StudentProfile, Job, Application

student = Blueprint("student", __name__)


# -----------------------------
# AUTH MIDDLEWARE
# -----------------------------
def require_student():
    if "user_id" not in session or session.get("role") != "student":
        return redirect("/login")
    return None


# -----------------------------
# DASHBOARD PAGE
# -----------------------------
@student.route("/dashboard", methods=["GET"])
def dashboard():
    auth = require_student()
    if auth:
        return auth

    user = User.query.get(session["user_id"])

    return render_template("student/dashboard.html", user=user)


# -----------------------------
# GET PROFILE
# -----------------------------
@student.route("/profile", methods=["GET"])
def get_profile():
    auth = require_student()
    if auth:
        return auth

    profile = StudentProfile.query.filter_by(user_id=session["user_id"]).first()
    user = User.query.get(session["user_id"])

    return render_template("student/profile.html", user=user, profile=profile)


# UPDATE PROFILE
# -----------------------
@student.route("/profile", methods=["POST"])
def update_profile():
    auth = require_student()
    if auth:
        return auth

    profile = StudentProfile.query.filter_by(user_id=session["user_id"]).first()

    profile.department = request.form.get("department", profile.department)
    profile.year = request.form.get("year", profile.year)
    profile.cgpa = request.form.get("cgpa", profile.cgpa)
    profile.resume_link = request.form.get("resume_link", profile.resume_link)

    db.session.commit()
    return redirect("/student/profile")


# -----------------------------
# LIST JOBS
# -----------------------------
@student.route("/jobs", methods=["GET"])
def list_jobs():
    auth = require_student()
    if auth:
        return auth

    jobs = Job.query.all()

    return render_template("student/jobs.html", jobs=jobs)


# -----------------------------
# APPLY FOR JOB
# -----------------------------
@student.route("/apply/<int:job_id>", methods=["POST"])
def apply(job_id):
    auth = require_student()
    if auth:
        return auth

    student_id = session["user_id"]

    exists = Application.query.filter_by(
        job_id=job_id, student_id=student_id
    ).first()

    if exists:
        return redirect("/student/jobs?error=Already applied")

    new_app = Application(student_id=student_id, job_id=job_id)
    db.session.add(new_app)
    db.session.commit()

    return redirect("/student/jobs?success=Applied successfully")


# -----------------------------
# VIEW APPLICATIONS
# -----------------------------
@student.route("/applications", methods=["GET"])
def applications():
    auth = require_student()
    if auth:
        return auth

    apps = Application.query.filter_by(student_id=session["user_id"]).all()

    return render_template("student/applications.html", applications=apps)
