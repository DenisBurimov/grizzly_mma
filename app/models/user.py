import os
import base64
from datetime import datetime
import enum
from sqlalchemy import Enum
import onetimepass

from flask_login import UserMixin, AnonymousUserMixin
from sqlalchemy import func
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import relationship
from werkzeug.security import generate_password_hash, check_password_hash
from flask import current_app

from app import db
from app.models.utils import ModelMixin


def gen_secret_key():
    return base64.b32encode(os.urandom(20)).decode("utf-8")


class User(db.Model, UserMixin, ModelMixin):

    __tablename__ = "users"

    class Role(enum.Enum):
        """Utility class to support
        admin - creates users, including admins
        reseller - creates accounts and billings
        """

        admin = 1
        reseller = 2

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    role = db.Column(Enum(Role), default=Role.reseller)
    created_at = db.Column(db.DateTime, default=datetime.now)
    deleted = db.Column(db.Boolean, default=False)
    otp_secret = db.Column(db.String(32), default=gen_secret_key)
    otp_active = db.Column(db.Boolean, default=False)

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

    def get_totp_uri(self):
        """generate authentication URI for Google Authenticator"""
        APP_NAME = current_app.config["APP_NAME"]
        return f"otpauth://totp/{APP_NAME}:{self.username}?secret={self.otp_secret}&issuer={APP_NAME}"

    def verify_totp(self, token):
        """validates 6-digit OTP code retrieved from Google"""
        return onetimepass.valid_totp(token, self.otp_secret)

    def __repr__(self):
        return f"<{self.id}: {self.username} ({self.role})>"


class AnonymousUser(AnonymousUserMixin):
    pass
