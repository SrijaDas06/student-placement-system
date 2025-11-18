from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()


# -----------------------
# USER TABLE
# -----------------------
class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(50), nullable=False)   # student / admin
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationship to StudentProfile
    profile = db.relationship("StudentProfile", backref="user", uselist=False)


# -----------------------
# STUDENT PROFILE
# -----------------------
class StudentProfile(db.Model):
    __tablename__ = "student_profiles"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))

    department = db.Column(db.String(100))
    year = db.Column(db.String(20))
    cgpa = db.Column(db.Float)
    resume_link = db.Column(db.String(500))


# -----------------------
# COMPANIES
# -----------------------
class Company(db.Model):
    __tablename__ = "companies"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    jobs = db.relationship("Job", backref="company", cascade="all, delete-orphan")


# -----------------------
# JOBS
# -----------------------
class Job(db.Model):
    __tablename__ = "jobs"

    id = db.Column(db.Integer, primary_key=True)
    company_id = db.Column(db.Integer, db.ForeignKey("companies.id"))
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    salary = db.Column(db.String(100))
    posted_at = db.Column(db.DateTime, default=datetime.utcnow)

    applications = db.relationship("Application", backref="job", cascade="all, delete-orphan")


# -----------------------
# APPLICATIONS
# -----------------------
class Application(db.Model):
    __tablename__ = "applications"

    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey("users.id"))  # student user ID
    job_id = db.Column(db.Integer, db.ForeignKey("jobs.id"))
    applied_at = db.Column(db.DateTime, default=datetime.utcnow)
    status = db.Column(db.String(50), default="Pending")  # Pending / Accepted / Rejected
