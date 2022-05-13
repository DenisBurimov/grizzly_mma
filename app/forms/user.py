from flask_wtf import FlaskForm
from wtforms import IntegerField, StringField, PasswordField, SubmitField, SelectField
from wtforms.validators import DataRequired, InputRequired, EqualTo, ValidationError
from app.models import User


ROLES = [
    (User.Role.admin.value, User.Role.admin.name),
    (User.Role.reseller.value, User.Role.reseller.name),
]

FORBIDDEN_SYMBOLS = [
    "!",
    "@",
    "#",
    "%",
    "^",
    "&",
    "*",
    "(",
    ")",
    ":",
    ";",
    "<",
    ">",
    "?",
    ",",
    "/",
    "|",
    "\\",
    "*",
    "+",
    "'",
    '"',
    " ",
]


class UserForm(FlaskForm):
    username = StringField("Username", [DataRequired()])
    password = PasswordField("Password", [DataRequired()])
    password_confirm = PasswordField(
        "Confirm Password",
        validators=[
            DataRequired(),
            EqualTo("password", message="Password do not match."),
        ],
    )
    role = SelectField("Role", coerce=int, validators=[InputRequired()], choices=ROLES)
    submit = SubmitField("Add User")

    def validate_username(self, field):
        if User.query.filter_by(username=field.data).first() is not None:
            raise ValidationError("This username is taken.")

        for symbol in FORBIDDEN_SYMBOLS:
            if symbol in self.username.data:
                raise ValidationError("Forbidden symbols in username")


class UserUpdateForm(FlaskForm):
    username = StringField("Username", [DataRequired()])
    password = PasswordField("Password", [DataRequired()])
    password_confirm = PasswordField(
        "Confirm Password",
        validators=[
            DataRequired(),
            EqualTo("password", message="Password do not match."),
        ],
    )
    role = SelectField("Role", coerce=int, validators=[InputRequired()], choices=ROLES)
    submit = SubmitField("Update")

    def validate_username(self, field):

        for symbol in FORBIDDEN_SYMBOLS:
            if symbol in self.username.data:
                raise ValidationError("Forbidden symbols in username")


class UserFinanceForm(FlaskForm):
    username = StringField("Username", [DataRequired()])
    credits = IntegerField("Credits", [DataRequired()], default=0)
    transaction_type = SelectField(
        "Deposit/Withdraw", choices=[("Deposit", "Deposit"), ("Withdraw", "Withdraw")]
    )
    transaction_amount = IntegerField("Transaction", default=100)
    package_500_cost = IntegerField("500 messages cost", [DataRequired()])
    package_1000_cost = IntegerField("1000 messages cost", [DataRequired()])
    package_1500_cost = IntegerField("1500 messages cost", [DataRequired()])
    package_2500_cost = IntegerField("2500 messages cost", [DataRequired()])
    submit = SubmitField("Update")
