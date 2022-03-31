from datetime import datetime
from email.policy import default

from flask_login import UserMixin, AnonymousUserMixin
from sqlalchemy import func
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import relationship
from werkzeug.security import generate_password_hash, check_password_hash

from app import db
from app.models.utils import ModelMixin


class User(db.Model, UserMixin, ModelMixin):

    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    role = db.Column(db.String(64))  # TODO: Enum
    created_at = db.Column(db.DateTime, default=datetime.now)
    deleted = db.Column(db.Boolean, default=False)
    
    accounts = relationship("Account", viewonly=True)
    billings = relationship("Billing", viewonly=True)

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
        return f"<{self.id}: {self.username}>"

# TODO: install and configure
# TODO: Each class in separate file

class Account(db.Model, ModelMixin):
    
    __tablename__ = "accounts"
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    login = db.Column(db.String(16), unique=True, nullable=False)
    password = db.Column(db.String(16), nullable=False)
    
    def __repr__(self):
        return f"<{self.account_id}. {self.reseller}"
    
    
class Billing(db.Model, ModelMixin):
    
    __tablename__ = "billings"
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    credits = db.Column(db.Integer)
    created_at = db.Column(db.DateTime, default=datetime.now)
    
    reseller = relationship("User")
    
    def __repr__(self):
        return f"<{self.id}, reseller: {self.reseller}, credits: {self.credits}, created: {self.created_at}"
    

# class History(db.Model, ModelMixin):
#     id = db.Column(db.Integer, primary_key=True)
#     instance = db.Column(db.String(64), nullable=False)
#     created_by = db.Column(db.String(64), nullable=False)
#     created_at = db.Column(db.DateTime, default=datetime.now)
    
#     def __repr__(self):
#         return f"<{self.id}, instance: {self.instance}, created_by: {self.created_by}, created_at: {self.created_at}"
