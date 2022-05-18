import enum
from sqlalchemy import Enum
from sqlalchemy.orm import relationship
from datetime import datetime
from app import db
from app.models.utils import ModelMixin


class Transaction(db.Model, ModelMixin):

    __tablename__ = "transactions"

    class Action(enum.Enum):
        """
        Utility class to detect transaction type

        """

        deposit = "deposit"
        withdraw = "withdraw"

    id = db.Column(db.Integer, primary_key=True)
    action = db.Column(Enum(Action), default=Action.deposit)
    admin_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    transaction_amount = db.Column(db.Integer, default=0)
    reseller_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    created_at = db.Column(db.DateTime, default=datetime.now)
    comment = db.Column(db.String(120), default="Standart transaction")

    admin = relationship(
        "User",
        foreign_keys=[admin_id],
    )
    reseller = relationship(
        "User",
        foreign_keys=[reseller_id],
    )

    def __repr__(self):
        return f"<{self.id}, {self.admin_id}-{self.reseller_id} amount: {self.transaction_amount}>"
