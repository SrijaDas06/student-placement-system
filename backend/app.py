from flask import Flask
from models import db
from routes.auth import auth
from routes.student import student
from routes.admin import admin

app = Flask(__name__)
app.secret_key = "your-secret-key"

# DATABASE CONFIG
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///placement.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)

# CREATE TABLES
with app.app_context():
    db.create_all()

# REGISTER BLUEPRINTS
app.register_blueprint(auth)           # no url_prefix
app.register_blueprint(student, url_prefix="/student")
app.register_blueprint(admin, url_prefix="/admin")

if __name__ == "__main__":
    app.run(debug=True)
