import pytest
from flask_app.models import User, Match
from utils import add_user


def test_teacher_init():
    user = User(role="group_leader", email="test@test.com", password="password")
    assert user.role == "group_leader"
    assert user.email == "test@test.com"


def test_post_teacher(session):
    user = User(role="group_leader", email="test@test.com", password="password")
    session.add(user)
    session.commit()
    assert user.role.name == "group_leader"
    assert user.email == "test@test.com"
    assert user.id > 0


def test_post_match(session):
    user = add_user("group_leader", "test_teacher@test_teacher.com", "password")
    match = Match(
        leader_id=user.id,
        name="Match Nickname",
        school_district="dist",
        city="Philadelphia",
        state="PA",
        country="US",
        time_zone="EST",
        monday_start_time="09:00",
        scientist_preferred_type="marine biiology",
    )
    session.add(match)
    session.commit()
    assert match.id > 0
    assert match.name == "Match Nickname"


def test_post_match_by_scientist(session):
    user = add_user("scientist", "test_teacher@test_teacher.com", "password")
    with pytest.raises(Exception) as excinfo:
        # Should throw exception because scientists can't create Matches, they can only be assigned
        match = Match(
            leader_id=user.id,
            name="Match Nickname",
            school_district="dist",
            city="Philadelphia",
            state="PA",
            country="US",
            time_zone="EST",
            monday_start_time="09:00",
            scientist_preferred_type="marine biiology",
        )


def test_teacher_group_relationship(session):
    user = User(role="group_leader", email="test@test.com", password="password")
    session.add(user)
    session.commit()
    group = Match(
        leader_id=1,
        name="Group Nickname",
        school_district="dist",
        city="Philadelphia",
        state="PA",
        country="US",
        time_zone="EST",
        monday_start_time="09:00",
        scientist_preferred_type="marine biiology",
    )
    session.add(group)
    session.commit()
    group = Match.query.filter(Match.name == "Group Nickname").first()
    assert group.leader_id == user.id
