from flask_login import current_user
from flask_app.views.forms import RegisterMatchForm
from flask_app.models import User, Match
from utils import add_user, login, logout, add_match


def test_create_match(client, session, test_with_authenticated_user):
    assert client.get("/login").status_code == 200

    role = "group_leader"
    email = "create_match@create_match.com"
    password = "fake_password"

    add_user(role, email, password)
    login_res = login(client, email, password)

    assert (
        client.get("/matches/matches").status_code == 200
    ), "The matches page was not available"

    assert (
        client.get("/matches/register").status_code == 200
    ), "register match page not available"

    form = RegisterMatchForm(
        name="testgroup1",
        school_district="Philadelphia district",
        city="Philadelphia",
        state="Pennsylvania",
        country="US",
        time_zone="EST",
        monday_start_time="09:00",
        scientist_preferred_type="cool ones",
    )
    create_group_res = client.post("/matches/register", data=form.data)
    assert (
        create_group_res.status_code == 302
    ), f"expected status_code 302 for redirect for successfully creating group, but got {create_group_res.status_code}."

    assert (
        "http://localhost/matches/matches" == create_group_res.headers["Location"]
    ), "registration response header did not redictrt to 'matches/matches as expected"

    g = Match.query.filter(Match.name == form.name.data).first()
    user = User.query.filter(User.email == email).first()
    assert g.id > 0
    assert g.leader_id == user.id
    assert g.scientist_id is None, "There should be no scientist connected at this time"
    _ = logout(client)


def test_add_scientist_to_match(client, session, test_with_authenticated_user):
    assert client.get("/login").status_code == 200

    role = "group_leader"
    email = "create_match@create_match.com"
    password = "fake_password"

    gl = add_user(role, email, password)

    scientist = add_user("scientist", "sciencematch@sciencematch.com", "fake_password")

    _ = login(client, email, password)

    form = RegisterMatchForm(
        name="testgroup1",
        school_district="Philadelphia district",
        city="Philadelphia",
        state="Pennsylvania",
        country="US",
        time_zone="EST",
        monday_start_time="09:00",
        scientist_preferred_type="cool ones",
    )

    match = add_match(gl, form.data)

    assert match.scientist_id is None, "should be no scientist on match at this point"

    match.scientist_id = scientist.id

    check_match = Match.query.filter(Match.scientist_id == scientist.id).first()
    assert check_match.scientist_id == scientist.id
    assert check_match.leader_id == gl.id
