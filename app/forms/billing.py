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

    users_public_key = TextAreaField("User's public key", [DataRequired()])

    credits = SelectField(
        "Amount", coerce=int, validators=[InputRequired()], choices=PAY_OPTIONS
    )

    submit = SubmitField("Get credits")
