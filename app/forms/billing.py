from flask_wtf import FlaskForm
from wtforms import TextAreaField, SubmitField, SelectField
from wtforms.validators import InputRequired, DataRequired


class BillingForm(FlaskForm):
    PAY_OPTIONS = [
        (25, 25),
        (500, 500),
        (1000, 1000),
        (1500, 1500),
        (2500, 2500),
    ]

    RESELLERS_ACCOUNTS = [
        # (1, 1),
        # (2, 2),
    ]

    users_public_key = TextAreaField("User's public key", [DataRequired()])

    account = SelectField(
        "Account", coerce=int, validators=[InputRequired()], choices=RESELLERS_ACCOUNTS
    )

    credits = SelectField(
        "Amount",
        coerce=int,
        validators=[InputRequired()],
        choices=PAY_OPTIONS,
    )

    submit = SubmitField("Get credits")
