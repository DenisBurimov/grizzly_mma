from flask import Blueprint, redirect, url_for, render_template, request
from flask_login import current_user, login_required
from app.models import User

main_blueprint = Blueprint("main", __name__)


@main_blueprint.route("/")
@login_required
def index():
    if current_user.role == User.Role.admin:
        return redirect(url_for("users.users_page"))
    return redirect(url_for("accounts.accounts_page"))


@main_blueprint.route("/qrscanner", methods=["GET", "POST"])
@login_required
def qrscanner():
    qr_data = None
    if request.method == "POST":
        qr_data = request.form["qr_data"]
    return render_template("qrscanner.html", info=qr_data)
