from flask import Blueprint, render_template, url_for, redirect, flash, request
from flask_login import login_user, logout_user, login_required

from app.models import User
from app.forms import LoginForm
from app.logger import log

auth_blueprint = Blueprint("auth", __name__)


@auth_blueprint.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm(request.form)
    if form.validate_on_submit():
        user = User.authenticate(form.username.data, form.password.data)
        if user is not None:
            login_user(user)
            flash("You are successfuly logged in!", "info")
            return redirect(url_for("main.index"))
        flash("Wrong username or password.", "danger")
        log(log.ERROR, "Wrong username or password")
    return render_template("auth/login.html", form=form)


@auth_blueprint.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("main.index"))
