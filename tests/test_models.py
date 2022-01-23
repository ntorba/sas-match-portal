from flask_app.models import User, Group


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


def test_post_group(session):
    group = Group(
        user_id=1,
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
    assert group.id > 0
    assert group.name == "Group Nickname"


def test_teacher_group_relationship(session):
    user = User(role="group_leader", email="test@test.com", password="password")
    session.add(user)
    session.commit()
    group = Group(
        user_id=1,
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
    group = Group.query.filter(Group.name == "Group Nickname").first()
    assert group.user_id == user.id
