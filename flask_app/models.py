# project/models.py
# originall taken from https://github.com/mjhea0/flask-basic-registration/blob/master/project/models.py

import datetime
import enum
from sqlalchemy import Integer, Enum

from .extensions import db, bcrypt


class Role(enum.Enum):
    group_leader = 1
    scientist = 2
    admin = 3


class User(db.Model):

    # __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    role = db.Column(db.Enum(Role), nullable=False)
    name = db.Column(db.String, nullable=True)
    email = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)
    registered_on = db.Column(db.DateTime, nullable=False)
    admin = db.Column(db.Boolean, nullable=False, default=False)
    pronouns = db.Column(db.String)
    scienist_group = db.Column(db.String)
    career_stage = db.Column(db.String)
    time_zone = db.Column(db.String)
    science_category = db.Column(db.String)
    time_zone = db.Column(db.String)
    keywrods = db.Column(db.String)
    # availability = db.Column(db.String), TODO, find a better system for this
    languages = db.Column(db.String)
    background = db.Column(db.String)
    do_not_match_groups = db.Column(db.String)
    open_to_faith_affiliation = db.Column(db.Boolean)
    searchable = db.Column(db.Boolean)
    instagram_photo = db.Column(db.LargeBinary)
    instagram_caption = db.Column(db.String)
    discovery_medium = db.Column(db.String)
    group_organization = db.Column(db.String)
    commitment = db.Column(db.Boolean)
    receive_emails = db.Column(db.Boolean)
    code_of_conduct = db.Column(db.Boolean)
    profile_finished = db.Column(db.Boolean, default=False)

    def __init__(self, password, *args, admin=False, **kwargs):
        self.password = bcrypt.generate_password_hash(password)
        self.registered_on = datetime.datetime.now()
        self.admin = admin
        super().__init__(*args, **kwargs)

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return self.id

    def __repr__(self):
        return "<email {}".format(self.email)


class Match(db.Model):
    __tablename__ = "match"

    id = db.Column(db.Integer, primary_key=True)

    leader_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    scientist_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=True)
    leader = db.relationship("User", foreign_keys=[leader_id])
    scientist = db.relationship("User", foreign_keys=[scientist_id])

    # leader = db.relationship("User", back_populates="match", foreign_keys=[leader_id])
    # scientist = db.relationship(
    #     "User", back_populates="match", foreign_keys=[scientist_id]
    # )

    name = db.Column(db.String, unique=True, nullable=False)
    school_district = db.Column(db.String, nullable=False)
    city = db.Column(db.String, nullable=False)
    state = db.Column(db.String, nullable=True)
    country = db.Column(db.String, nullable=True)
    time_zone = db.Column(db.String, nullable=True)
    monday_start_time = db.Column(db.String, nullable=True)
    scientist_preferred_type = db.Column(db.String, nullable=True)
    registered_on = db.Column(db.DateTime, nullable=False)

    def __init__(
        self,
        leader_id,
        *args,
        **kwargs,
    ):
        leader = User.query.filter(User.id == leader_id).first()
        if leader.role.name != "group_leader":
            raise Exception(
                f"Matches must be created by group leaders! This user is role {leader.role.name}"
            )
        self.leader_id = leader_id
        self.registered_on = datetime.datetime.utcnow()

        super().__init__(*args, **kwargs)
