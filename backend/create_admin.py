from getpass import getpass
from werkzeug.security import generate_password_hash
from app import app
from models import db, User

def create_admin():
    name = input("Admin name: ").strip()
    email = input("Admin email: ").strip()
    password = getpass("Admin password (hidden): ").strip()
    if not name or not email or not password:
        print("Name, email and password are required.")
        return

    with app.app_context():
        if User.query.filter_by(email=email).first():
            print("A user with that email already exists.")
            return
        hashed = generate_password_hash(password)
        user = User(name=name, email=email, password=hashed, role='admin')
        db.session.add(user)
        db.session.commit()
        print("Admin created. ID:", user.id)

if __name__ == '__main__':
    create_admin()
