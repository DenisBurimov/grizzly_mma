from flask_wtf import FlaskForm
from wtforms import SubmitField, SelectField
from wtforms.validators import InputRequired


class BillingForm(FlaskForm):
    PAY_OPTIONS = [
        (25, 25),
        (500, 500),
        (1000, 1000),
        (1500, 1500),
        (2500, 2500),
    ]
    credits = SelectField(
        "Amount", coerce=int, validators=[InputRequired()], choices=PAY_OPTIONS
    )

    submit = SubmitField("Get credits")
