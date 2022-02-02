# project/user/forms.py
# originally taken from https://github.com/mjhea0/flask-basic-registration/blob/master/project/user/forms.py
from pathlib import Path
from tkinter.tix import Select
from xmlrpc.client import Boolean
import pytz
from flask_wtf import FlaskForm
from wtforms import (
    StringField,
    PasswordField,
    SelectField,
    SelectMultipleField,
    DateTimeField,
    BooleanField,
    FileField,
)
from wtforms.validators import DataRequired, Email, Length, EqualTo

from ..models import User
from ..extensions import bcrypt


class LoginForm(FlaskForm):
    email = StringField("email", validators=[DataRequired(), Email()])
    password = PasswordField("password", validators=[DataRequired()])

    def validate(self):
        initial_validation = super(LoginForm, self).validate()
        if not initial_validation:
            return False
        user = User.query.filter_by(email=self.email.data).first()
        if user is None:
            self.email.errors.append("This email is not found in our records")
            return False
        else:
            if user and bcrypt.check_password_hash(user.password, self.password.data):
                return True
            else:
                self.password.errors.append("This password does not match email.")
                return False


with open(Path(__file__).parent.parent / "states.txt", "r") as f:
    STATES = [i.strip("\n") for i in f.readlines()]


class RegisterUserForm(FlaskForm):
    role = SelectField(
        "Your Role (Group Leader or Scientist)", choices=["group_leader", "scientist"]
    )
    email = StringField(
        "Email", validators=[DataRequired(), Email(message=None), Length(min=6, max=40)]
    )
    confirm_email = StringField(
        "Confirm Email",
        validators=[
            DataRequired(),
            Email(message=None),
            Length(min=6, max=40),
            EqualTo("email", message="Make sure your email entries match"),
        ],
    )
    password = PasswordField(
        "Password", validators=[DataRequired(), Length(min=6, max=25)]
    )
    confirm_password = PasswordField(
        "Repeat Password",
        validators=[
            DataRequired(),
            EqualTo("password", message="Passwords must match."),
        ],
    )

    def validate(self):
        initial_validation = super(RegisterUserForm, self).validate()
        if not initial_validation:
            return False
        user = User.query.filter_by(email=self.email.data).first()
        if user:
            self.email.errors.append("Email already registered")
            return False
        return True


class ForgotPasswordForm(FlaskForm):
    email = StringField(
        "Email", validators=[DataRequired(), Email(message=None), Length(min=6, max=40)]
    )


class RegisterMatchForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired(), Length(max=40)])
    school_district = StringField("School District", validators=[])
    city = StringField("City", validators=[])
    state = SelectField("State", choices=STATES, validators=[])
    country = SelectField("Country", choices=["US", "CA"], validators=[])
    time_zone = SelectField("Timezone", choices=pytz.all_timezones_set, validators=[])
    monday_start_time = DateTimeField("Monday Start Time", format="%H:%M")
    scientist_preferred_type = SelectField(
        "Preferred Scientist Type",
        choices=[
            "cool ones"
        ],  # TODO: Query the db to pull out all available types of scientsists from those that have signed up
    )


class GroupLeaderUpdateProfileForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired(), Length(max=100)])
    email = StringField(
        "Email", validators=[DataRequired(), Email(message=None), Length(min=6, max=40)]
    )


with open("scientist_fields.txt") as f:
    SCIENTIST_CATEGORIES = [i.strip("\n") for i in f.readlines()]

with open("languages.txt") as f:
    LANGUAGES = [i.strip("\n") for i in f.readlines()]

with open("racial_background.txt") as f:
    BACKGROUNDS = [i.strip("\n") for i in f.readlines()]

with open("match_groups.txt"):
    DO_NOT_MATCH_GROUPS = [i.strip("\n") for i in f.readlines()]

with open("discovery_mediums.txt"):
    DISCOVERY_MEDIUMS = [i.strip("\n") for i in f.readlines()]


class ScientistProfileForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired(), Length(max=100)])
    email = StringField(
        "Email", validators=[DataRequired(), Email(message=None), Length(min=6, max=40)]
    )
    pronouns = SelectField(
        "Pronouns",
        choices=["He/Him", "She/Her", "They/Them", "Other"],
    )
    group = StringField(  # University/Institute/Company/Hospital/etc
        "Group/University/Company/Hospital/etc.", validators=[DataRequired()]
    )
    career_stage = SelectField(
        "Career Stage",
        choices=[
            "Graduate Student (Masters/phD)",
            "Post-doc",
            "Professor",
            "Industry Scientist",
            "Professional scientist",
        ],
    )
    time_zone = SelectField("Timezone", choices=pytz.all_timezones_set, validators=[])
    science_category = SelectMultipleField(
        "Science Category", choices=SCIENTIST_CATEGORIES
    )
    keywords = StringField("keywords")
    num_classrooms = SelectField(
        "Number of classrooms to be matched with", choices=list(range(1, 6))
    )
    availability = None  # TODO
    languages = SelectField(
        "Language",  # TODO: Make the other option dynamic and ready for user input
        choices=LANGUAGES,
    )
    background = SelectField(
        "Language",  # TODO: Make the other option dynamic and ready for user input
        choices=BACKGROUNDS,
    )
    do_not_match_groups = SelectField(
        "Language",  # TODO: Make the other option dynamic and ready for user input
        choices=DO_NOT_MATCH_GROUPS,
    )
    open_to_faith_affiliation = BooleanField("Open to faith affiliation")
    reminders = BooleanField("Would you like to opt into reminders after signup?")
    searchable = BooleanField(
        "Would you like to be included on a searchable list of scientists? This will include your name, time zone, and keywords"
    )
    instagram_photo = FileField("Instagram feature photo")
    instagram_caption = StringField(
        "For instagram: Introduce yourself, including what you work on in simple terms. This will caption the instagram post. Include your handle if you want to be tagged!"
    )
    discovery_medium = SelectField(
        "How did you hear about Skype a Scientist?", choices=DISCOVERY_MEDIUMS
    )
    group_organization = SelectField(
        "If you are part of an organization that is participating as a group, please select the name of your group here",
        choices=["USP", "Illumina", "Other"],
    )
    commitment = BooleanField(
        "I commit to either contacting my matched teacher or e-mail skypeascientist@gmail.com to report a problem *"
    )
    receive_emails = BooleanField(
        "Please click this box to confirm that you are willing to receive e-mails from Skype a Scientist. *"
    )
    code_of_conduct = StringField(
        "We require our scientists and groups to abide by a code of conduct. The scientist code of conduct can be found here: http://bit.ly/Sci_Conduct_Code Please type your name to confirm that you agree to abide by the code of conduct. *",
        validators=[DataRequired()],
    )


class ChangePasswordForm(FlaskForm):
    password = PasswordField(
        "password", validators=[DataRequired(), Length(min=6, max=25)]
    )
    confirm = PasswordField(
        "Repeat password",
        validators=[
            DataRequired(),
            EqualTo("password", message="Passwords must match."),
        ],
    )
