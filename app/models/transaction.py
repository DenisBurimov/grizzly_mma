import enum
from sqlalchemy import Enum
from sqlalchemy.orm import relationship
from datetime import datetime
from app import db
from app.models.utils import ModelMixin


class Transaction(db.Model, ModelMixin):

    __tablename__ = "transactions"

    class Action(enum.IntEnum):
        """
        Utility class to detect transaction type

        """

        deposit = 1
        withdraw = 2

    id = db.Column(db.Integer, primary_key=True)
    action = db.Column(Enum(Action), default=Action.deposit)
    admin_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    transaction_amount = db.Column(db.Integer, default=0)
    reseller_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    created_at = db.Column(db.DateTime, default=datetime.now)
    comment = db.Column(db.String(120), default="Standart transaction")

    admin = relationship("User", foreign_keys=[admin_id])
    reseller = relationship("User", foreign_keys=[reseller_id])

    def __repr__(self):
        return f"<{self.id}, instance: {self.admin_username}, created_by: {self.transaction_amount}"
