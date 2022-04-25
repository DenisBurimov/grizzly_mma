from flask_wtf import FlaskForm
from wtforms import SubmitField, IntegerField
from wtforms.validators import DataRequired


class BillingForm(FlaskForm):
    credits = IntegerField("Amount", [DataRequired()])

    submit = SubmitField("Get credits")
