from flask import render_template, request, redirect, Blueprint, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user

from ..models import User, Group
from ..extensions import db
from .forms import RegisterMatchForm

matches_blueprint = Blueprint(
    "matches", __name__, url_prefix="/matches", template_folder="templates"
)


@matches_blueprint.route("/register", methods=["GET", "POST"])
@login_required
def register_match():
    form = RegisterMatchForm(request.form)
    if request.method == "GET":
        return render_template("register-classroom.html", form=form)
    last_class = Group.query.first()
    if form.validate_on_submit():
        ## TODO: Think of check for repeat classrooms
        user = User.query.filter_by(email=current_user.email).first()
        group = Group(user_id=user.id, **form.data)
        db.session.add(group)
        db.session.commit()
        flash(f"Successfully added classroom {form.name.data}!", "success")
        return f"successfully added match {group.name}", 201
    else:
        return f"failed to create group with errors: {form.errors}", 400


@matches_blueprint.route("/matches", methods=["GET", "POST"])
@login_required
def matches():
    matches = Group.query.filter(Group.user_id == current_user.id).all()
    return render_template("matches.html", matches=matches)


@matches_blueprint.route("/classroom/<classroomid>", methods=["GET", "POST"])
@login_required
def classroom(classroomid):
    return "fuuuuck"  # TODO make pages for a group (this is where they could give feedback)
