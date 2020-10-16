from db import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin, LoginManager
from login_manager import login_manager, login_user, login_required, logout_user

@login_manager.user_loader
def load_user(id):
    return Users.query.get(int(id))

class Users(db.Model, UserMixin):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(16), unique=True, index=True)
    password = db.Column(db.String(128))

    def __init__(self, username, password):
        hashed = generate_password_hash(password)
        self.username = username
        self.password = hashed

    def __repr__(self):
        return f"Username {username} exists in database"

    @classmethod
    def find_by_username(cls, username):
        return Users.query.filter_by(username=username).first()

    def check_credentials(self, password):
        return check_password_hash(self.password, password)

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
