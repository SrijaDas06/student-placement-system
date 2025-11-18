from flask import Blueprint, request, jsonify, session, render_template, redirect
from models import db, User, Company, Job, Application, StudentProfile

admin = Blueprint("admin", __name__)


# -----------------------------
# ADMIN MIDDLEWARE
# -----------------------------
def require_admin():
    if "user_id" not in session or session.get("role") != "admin":
        return redirect("/login")
    return None


# -----------------------------
# DASHBOARD
# -----------------------------
@admin.route("/dashboard", methods=["GET"])
def dashboard():
    auth = require_admin()
    if auth:
        return auth

    stats = {
        "students": User.query.filter_by(role="student").count(),
        "companies": Company.query.count(),
        "jobs": Job.query.count(),
        "applications": Application.query.count()
    }
    return render_template("admin/dashboard.html", stats=stats)


# -----------------------------
# LIST COMPANIES (Show template)
# -----------------------------
@admin.route("/companies", methods=["GET"])
def list_companies_page():
    auth = require_admin()
    if auth:
        return auth

    companies = Company.query.all()
    return render_template("admin/companies.html", companies=companies)


# ADD COMPANY (API endpoint)
# -----------------------------
@admin.route("/company", methods=["POST"])
def add_company():
    auth = require_admin()
    if auth:
        return auth

    name = request.json.get("name")

    if Company.query.filter_by(name=name).first():
        return jsonify({"error": "Company already exists"}), 400

    c = Company(name=name, description=request.json.get("description"))
    db.session.add(c)
    db.session.commit()

    return jsonify({"message": "Company added", "id": c.id})


# CREATE JOB (Show form)
# -----------------------
@admin.route("/add_job", methods=["GET"])
def create_job_page():
    auth = require_admin()
    if auth:
        return auth

    companies = Company.query.all()
    return render_template("admin/create_job.html", companies=companies)


# CREATE JOB (API)
# -----------------------
@admin.route("/job", methods=["POST"])
def create_job():
    auth = require_admin()
    if auth:
        return auth

    data = request.json

    job = Job(
        title=data.get("title"),
        description=data.get("description"),
        salary=data.get("salary"),
        company_id=data.get("company_id"),
    )

    db.session.add(job)
    db.session.commit()

    return jsonify({"message": "Job created", "id": job.id})


# -----------------------
# LIST JOBS (Show template)
# -----------------------
@admin.route("/jobs", methods=["GET"])
def list_jobs_page():
    auth = require_admin()
    if auth:
        return auth

    jobs = Job.query.all()
    return render_template("admin/jobs.html", jobs=jobs)


# -----------------------------
# DELETE JOB
# -----------------------------
@admin.route("/job/<int:job_id>", methods=["DELETE"])
def delete_job(job_id):
    auth = require_admin()
    if auth:
        return auth

    job = Job.query.get(job_id)

    if not job:
        return jsonify({"error": "Job not found"}), 404

    db.session.delete(job)
    db.session.commit()

    return jsonify({"message": "Job deleted"})


# -----------------------
# ALL APPLICATIONS (Show template)
# -----------------------
@admin.route("/applications", methods=["GET"])
def applications_page():
    auth = require_admin()
    if auth:
        return auth

    apps = Application.query.all()
    return render_template("admin/applications.html", applications=apps)


# -----------------------------
# VIEW STUDENT PROFILE (ADMIN)
# -----------------------------
@admin.route("/student/<int:user_id>", methods=["GET"])
def view_student(user_id):
    auth = require_admin()
    if auth:
        return auth

    user = User.query.get(user_id)
    if not user:
        return redirect('/admin/applications')

    profile = StudentProfile.query.filter_by(user_id=user_id).first()
    return render_template('admin/student_profile.html', user=user, profile=profile)


# -----------------------------
# UPDATE APPLICATION STATUS
# -----------------------------
@admin.route("/application/<int:app_id>", methods=["PUT"])
def update_application(app_id):
    auth = require_admin()
    if auth:
        return auth

    new_status = request.json.get("status")

    app = Application.query.get(app_id)

    if not app:
        return jsonify({"error": "Application not found"}), 404

    app.status = new_status
    db.session.commit()

    return jsonify({"message": "Status updated"})
