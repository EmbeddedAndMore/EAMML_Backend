from __future__ import annotations

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text
from werkzeug.security import check_password_hash, generate_password_hash

db = SQLAlchemy()


class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(128))
    email = db.Column(db.String(128), index=True)
    password_hash = db.Column(db.String(128))

    def hash_password(self, password: str) -> str:
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password: str) -> bool:
        return check_password_hash(self.password_hash, password)

    def check_exists(self):
        user = User.query.filter_by(username=self.username).first()
        return user is not None

    def get_user(self) -> User:
        return User.query.filter_by(username=self.username).first()

    def save(self):
        db.session.add(self)
        db.session.commit()
