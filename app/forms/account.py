from flask_wtf import FlaskForm
from wtforms import SubmitField, StringField
from wtforms.validators import DataRequired


class AccountForm(FlaskForm):
    login = StringField("Login", [DataRequired()])
    password = StringField("Password", [DataRequired()])

    submit = SubmitField("Save")
