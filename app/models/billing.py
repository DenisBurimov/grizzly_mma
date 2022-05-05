from datetime import datetime
from sqlalchemy.orm import relationship
from app import db
from app.models.utils import ModelMixin


class Billing(db.Model, ModelMixin):

    __tablename__ = "billings"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    account_id = db.Column(db.Integer, db.ForeignKey("accounts.id"))
    credits = db.Column(db.Integer)
    created_at = db.Column(db.DateTime, default=datetime.now)
    qrcode = db.Column(db.LargeBinary)

    reseller = relationship("User")
    account = relationship("Account")

    def __repr__(self):
        return f"<{self.id}, reseller: {self.reseller}, credits: {self.credits}, created: {self.created_at}"
