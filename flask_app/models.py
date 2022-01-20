# project/models.py
# originall taken from https://github.com/mjhea0/flask-basic-registration/blob/master/project/models.py

import datetime
from turtle import circle

from .extensions import db, bcrypt

# class Parent(Base):
#     __tablename__ = 'parent'
#     id = Column(Integer, primary_key=True)
#     child_id = Column(Integer, ForeignKey('child.id'))
#     child = relationship("Child", back_populates="parents")

# class Child(Base):
#     __tablename__ = 'child'
#     id = Column(Integer, primary_key=True)
#     parents = relationship("Parent", back_populates="child")

class User(db.Model):

    # __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    role = db.Column(db.String, nullable=False)
    name = db.Column(db.String, nullable=False)
    email = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)
    registered_on = db.Column(db.DateTime, nullable=False)
    admin = db.Column(db.Boolean, nullable=False, default=False)
    classroom = db.relationship("ClassRoom", back_populates="user") # THIS IS A LIST, CAN HAVE MULTIPLE

    def __init__(self, role, name, email, password, paid=False, admin=False):
        self.role = role
        self.name = name
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
        return '<email {}'.format(self.email)

class ClassRoom(db.Model):
    __tablename__ = "classroom"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship("User", back_populates="classroom")
    name = db.Column(db.String, unique=True, nullable=False)
    school_district = db.Column(db.String, unique=True, nullable=False)
    city = db.Column(db.String, nullable=False)
    state = db.Column(db.String, nullable=True)
    country = db.Column(db.String, nullable=True)
    time_zone = db.Column(db.String, nullable=True)
    monday_start_time = db.Column(db.String, nullable=True)
    scientist_preferred_type = db.Column(db.String, nullable=True)
    registered_on = db.Column(db.DateTime, nullable=False)

    def __init__(self, user_id, name, school_district, city, state, country, time_zone, monday_start_time, scientist_preferred_type, **kwargs):
        self.user_id = user_id
        self.name = name
        self.school_district = school_district
        self.city = city
        self.state = state 
        self.country = country
        self.time_zone = time_zone
        self.monday_start_time = monday_start_time
        self.scientist_preferred_type = scientist_preferred_type
        self.registered_on = datetime.datetime.utcnow()
        super().__init__()