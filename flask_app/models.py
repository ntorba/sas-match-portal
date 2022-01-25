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
    # match = db.relationship(
    #     "Match", back_populates="user"
    # )  # String THIS IS A LIST, CAN HAVE MULTIPLE

    def __init__(self, role, email, password, admin=False):
        self.role = role
        self.email = email
        self.password = bcrypt.generate_password_hash(password)
        self.registered_on = datetime.datetime.now()
        self.admin = admin
        super().__init__()

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
    school_district = db.Column(db.String, unique=True, nullable=False)
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
        name,
        school_district,
        city,
        state,
        country,
        time_zone,
        monday_start_time,
        scientist_preferred_type,
        scientist_id=None,
        **kwargs,
    ):
        leader = User.query.filter(User.id == leader_id).first()
        if leader.role.name != "group_leader":
            raise Exception(
                f"Matches must be created by group leaders! This user is role {leader.role.name}"
            )
        self.leader_id = leader_id
        self.name = name
        self.school_district = school_district
        self.city = city
        self.state = state
        self.country = country
        self.time_zone = time_zone
        self.monday_start_time = monday_start_time
        self.scientist_preferred_type = scientist_preferred_type
        self.scientist_id = scientist_id
        self.registered_on = datetime.datetime.utcnow()
        super().__init__()
