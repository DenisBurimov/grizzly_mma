from datetime import datetime
from sqlalchemy.orm import relationship
from app import db
from app.models.utils import ModelMixin


class Account(db.Model, ModelMixin):

    __tablename__ = "accounts"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    login = db.Column(db.String(16), unique=True, nullable=False)
    password = db.Column(db.String(16), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now)
    # deleted = db.Column(db.Boolean, default=False)

    user = relationship("User")

    def __repr__(self):
        return f"<{self.id}. user: {self.user_id}, created_at: {self.created_at}"
