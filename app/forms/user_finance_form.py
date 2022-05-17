from flask_wtf import FlaskForm
from wtforms import (
    IntegerField,
    StringField,
    SubmitField,
    SelectField,
    BooleanField,
)
from wtforms.validators import DataRequired
from app.models import Transaction


class UserFinanceForm(FlaskForm):
    TRANSACTION_TYPE = [
        (Transaction.Action.deposit.name, Transaction.Action.deposit.name),
        (Transaction.Action.withdraw.name, Transaction.Action.withdraw.name),
    ]

    username = StringField("Username")
    credits = IntegerField("Credits")
    package_500_cost = IntegerField("500 messages cost", [DataRequired()])
    package_1000_cost = IntegerField("1000 messages cost", [DataRequired()])
    package_1500_cost = IntegerField("1500 messages cost", [DataRequired()])
    package_2500_cost = IntegerField("2500 messages cost", [DataRequired()])
    credit_alowed = BooleanField("Negative balance")
    transaction_type = SelectField(
        "Deposit/Withdraw", choices=TRANSACTION_TYPE, coerce=Transaction.Action
    )
    transaction_amount = IntegerField("Transaction", default=0)
    comment = StringField("Comment")
    submit = SubmitField("Update")
