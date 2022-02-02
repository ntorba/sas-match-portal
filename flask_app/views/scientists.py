from flask import render_template, request, redirect, Blueprint, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user

from ..models import User, Match
from ..extensions import db
from .forms import RegisterMatchForm

scientists_blueprint = Blueprint(
    "scientists", __name__, url_prefix="/scientists", template_folder="templates"
)


@scientists_blueprint.route("/search", methods=["GET"])
def search():
    # scidata = cur.fetchall()
    scidata = User.query.filter(User.role == "scientist").all()
    return render_template("scientist-search.html", indata=scidata)
