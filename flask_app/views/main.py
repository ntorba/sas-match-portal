from flask import render_template, request, redirect, Blueprint, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user

from ..models import User, Match
from ..extensions import bcrypt, db
from .forms import (
    ChangePasswordForm,
)

main_blueprint = Blueprint("main", __name__, template_folder="templates")


@main_blueprint.route("/")
def index():
    if current_user.is_authenticated:
        return redirect(url_for("main.home"))
    return render_template("index.html")


@main_blueprint.route("/about/")
def about():
    return render_template("about.html")


@main_blueprint.route("/home")
@login_required
def home():
    classrooms = None
    events = []
    if current_user.role == "Teacher":
        classrooms = Match.query.filter(Match.leader_id == current_user.id).all()
    return render_template("home.html", classrooms=classrooms, events=events)


@main_blueprint.route("/profile")
@login_required
def profile():
    return render_template("profile.html")


@main_blueprint.route("/profile_update", methods=["GET", "POST"])
@login_required
def profile_update():
    form = ChangePasswordForm(request.form)
    if form.validate_on_submit():
        user = User.query.filter_by(email=current_user.email).first()
        if user:
            user.password = bcrypt.generate_password_hash(form.password.data)
            db.session.commit()
            flash("Password successfully changed.", "success")
            return redirect(url_for("user.profile"))
        else:
            flash("Password change was unsuccessful.", "danger")
            return redirect(url_for("user.profile"))
    return render_template("profile-update.html", form=form)
