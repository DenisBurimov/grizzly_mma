from flask_wtf import FlaskForm
from wtforms import PasswordField, SubmitField
from wtforms.validators import DataRequired


class AccountForm(FlaskForm):
    login = PasswordField("Login", [DataRequired()])
    password = PasswordField("Password", [DataRequired()])

    submit = SubmitField("Save")
