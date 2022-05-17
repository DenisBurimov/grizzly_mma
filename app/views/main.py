from flask import Blueprint, redirect, url_for
from flask_login import current_user, login_required
from app.models import User

main_blueprint = Blueprint("main", __name__)


@main_blueprint.route("/")
@login_required
def index():
    return redirect(url_for("billings.billings_page"))
