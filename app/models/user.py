from cgi import print_form
from datetime import datetime
from enum import unique

from flask_login import UserMixin, AnonymousUserMixin
from sqlalchemy import func
from sqlalchemy.ext.hybrid import hybrid_property
from werkzeug.security import generate_password_hash, check_password_hash

from app import db
from app.models.utils import ModelMixin


class User(db.Model, UserMixin, ModelMixin):

    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now)
    accounts = db.relationship("Account", backref="user", lazy=True)

    @hybrid_property
    def password(self):
        return self.password_hash

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    @classmethod
    def authenticate(cls, username, password):
        user = cls.query.filter(
            func.lower(cls.username) == func.lower(username)
        ).first()
        if user and check_password_hash(user.password, password):
            return user

    def __repr__(self):
        return f"<user_id: {self.id}, username: {self.username}>"


class Account(db.Model):
    account_id = db.Column(db.Integer, primary_key=True)
    reseller = db.Column(db.String(64), db.ForeignKey("user.username"))
    login = db.Column(db.String(64), unique=True, nullable=False)
    password = db.Column(db.String(64), nullable=False)
    
    def __repr__(self):
        return f"account_id: {self.account_id}, reseller: {self.reseller}"
    
    
class Billing(db.Model):
    reseller = db.Column(db.String(64), db.ForeignKey("user.username"))
    credits = db.Column(db.Integer)
    created_at = db.Column(db.DateTime, default=datetime.now)
    
    def __repr__(self):
        return f"reseller: {self.reseller}, credits: {self.credits}, created: {self.created_at}"
    

class History(db.Model):
    instance = db.Column(db.String(64), nullable=False)
    created_by = db.Column(db.String(64), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now)
    
    def __repr__(self):
        return f"instance: {self.instance}, created_by: {self.created_by}, created_at: {self.created_at}"
