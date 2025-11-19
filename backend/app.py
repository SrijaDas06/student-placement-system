from flask import Flask
from models import db
from routes.auth import auth
from routes.student import student
from routes.admin import admin
from config import Config

app = Flask(__name__)
app.config.from_object(Config)

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
