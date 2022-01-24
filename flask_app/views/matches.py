from flask import render_template, request, redirect, Blueprint, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user

from ..models import User, Group
from ..extensions import db
from .forms import RegisterGroup

group_blueprint = Blueprint("group", __name__, template_folder="templates")


@group_blueprint.route("/register-group", methods=["GET", "POST"])
@login_required
def register_group():
    form = RegisterGroup(request.form)
    last_class = Group.query.first()
    if form.validate_on_submit():
        ## TODO: Think of check for repeat classrooms
        user = User.query.filter_by(email=current_user.email).first()
        classroom = Group(user_id=user.id, **form.data)
        db.session.add(classroom)
        db.session.commit()
        flash(f"Successfully added classroom {form.name.data}!", "success")
        return redirect(url_for("main.profile"))
    return render_template("register-classroom.html", form=form)


@group_blueprint.route("/classroom/<classroomid>", methods=["GET", "POST"])
@login_required
def classroom(classroomid):
    return "fuuuuck"  # TODO make pages for a group (this is where they could give feedback)
