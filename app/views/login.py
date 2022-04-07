from flask import (
    Blueprint,
    render_template,
    url_for,
    redirect,
    flash,
    request,
    current_app,
    session,
)
from flask_login import login_user, logout_user, login_required

from app.models import User
from app.forms import LoginForm
from app.logger import log

login_blueprint = Blueprint("login", __name__)


@login_blueprint.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm(request.form)
    if form.validate_on_submit():
        user: User = User.authenticate(form.username.data, form.password.data)
        flash("You are successfuly logged in!", "info")
        if user:
            if not current_app.config["AUTH_OTP_ENABLED"]:
                login_user(user)
                flash("Login successful.", "success")
                return redirect(url_for("main.index"))
            session["id"] = user.id
            # check if user has OTP activated
            if user.otp_active:
                log(log.INFO, "redirect to otp_verify")
                return redirect(url_for("auth.otp_verify"))

            # redirect to Two Factor Setup
            else:
                log(log.INFO, "user otp_status inactive")
                return redirect(url_for("auth.two_factor_warning"))
        flash("Wrong username or password.", "danger")
        log(log.ERROR, "Wrong username or password")
    return render_template("auth/login.html", form=form)


@login_blueprint.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("main.index"))
