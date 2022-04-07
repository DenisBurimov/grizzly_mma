from io import BytesIO
import pyqrcode
from flask import (
    Blueprint,
    render_template,
    url_for,
    redirect,
    flash,
    request,
    session,
)
from flask_login import login_user

from app import db
from app.models import User
from app.forms import TwoFactorForm
from app.logger import log


auth_blueprint = Blueprint("auth", __name__)


@auth_blueprint.route("/otp_verify", methods=["GET", "POST"])
def otp_verify():
    log(log.INFO, "/otp_verify")
    # check if user passed username & password verification
    if not session.get("id"):
        log(log.WARNING, "user auth_status not confirmed")
        flash("Please login to your account first", "danger")
        return redirect(url_for("login.login"))
    form = TwoFactorForm(request.form)
    if form.validate_on_submit():
        log(log.INFO, "otp form validated")
        user = User.query.get(session.get("id"))
        if user.verify_totp(form.token.data):
            log(log.INFO, f"user {user} logged opt validated")
            login_user(user)
            flash("You are successfuly logged in!", "info")

            # remove session data for added security
            del session["id"]

            log(log.INFO, "session cookie cleared")
            return redirect(url_for("main.index"))
        flash("Invalid OTP token. Try again.", "danger")
        log(log.WARNING, "Invalid OTP token")
    elif form.is_submitted():
        log(log.WARNING, f"OTP form validation error: {form.errors}")
    return render_template("auth/otp_form.html", form=form)


@auth_blueprint.route("/two_factor_warning")
def two_factor_warning():
    log(log.INFO, "/two_factor_warning")
    return render_template("auth/two_factor_warning.html")


@auth_blueprint.route("/two_factor_setup", methods=["GET", "POST"])
def two_factor_setup():
    log(log.INFO, "/two_factor_setup")
    form = TwoFactorForm(request.form)
    user_id = session.get("id", None)
    if not user_id:
        log(log.WARNING, "user_name not in session")
        flash("We could not verify your credentials. Please log in first.")
        return redirect(url_for("login.login"))
    user = User.query.filter(
        User.id == user_id, User.deleted == False  # noqa E712
    ).first()

    if request.method == "POST":
        if form.validate_on_submit() and user.verify_totp(form.token.data):
            return redirect(url_for("auth.otp_set_up_verification"))
        else:
            flash("Invalid OTP token. Please try again.", "danger")
            return redirect(url_for("auth.two_factor_setup"))
    # render QR code without caching it in browser
    if not user.otp_secret:
        user.otp_secret = User.gen_secret()
        user.save()
    return (
        render_template("auth/two-factor-setup.html", user=user, form=form),
        200,
        {
            "Cache-Control": "no-cache, no-store, must-revalidate",
            "Pragma": "no-cache",
            "Expires": "0",
        },
    )


@auth_blueprint.route("/qrcode")
def qrcode():
    if not session.get("id"):
        log(log.WARNING, "no such user id in session")
        flash("You do not have permissions to access this page.", "danger")
        return redirect(url_for("login.login"))
    user = User.query.get(session.get("id"))
    if user.otp_active:
        flash("Two-factor authentication is activated`. Please log in.", "warning")
        return redirect(url_for("login.login"))

    # render qrcode for Google Authenticator
    qrcode = pyqrcode.create(user.get_totp_uri())
    stream = BytesIO()
    qrcode.svg(stream, scale=3)
    return (
        stream.getvalue(),
        200,
        {
            "Content-Type": "image/svg+xml",
            "Cache-Control": "no-cache, no-store, must-revalidate",
            "Pragma": "no-cache",
            "Expires": "0",
        },
    )


@auth_blueprint.route("/otp_set_up_verification")
def otp_set_up_verification():
    """This route finalises 2FA process set up"""
    user = User.query.get(session.get("id"))
    # remove user id from session for added security
    if not user.otp_active:
        del session["id"]
        # update otp status in users DB
        user.otp_active = True
        user.save()
        flash(
            "Two-Factor Authentication is set up successfully. You can now log in.",
            "success",
        )
        return redirect(url_for("login.login"))
    flash("Two-Factor Authentication is active. Please log in.", "warning")
    return redirect(url_for("login.login"))
