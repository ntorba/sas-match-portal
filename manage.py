from flask.cli import FlaskGroup

from flask_app.app import create_app, db 
from flask_app.models import Group, User 

cli = FlaskGroup(create_app=create_app)

@cli.command()
def recreate_db():
    db.drop_all()
    db.create_all()
    db.session.commit()

@cli.command()
def seed_db():
    """Put some inital data in the database"""
    users = [
        User(
            role="Admin",
            name="admin",
            email = "admin@admin.com",
            password = "admins",
            admin=True
        ),
        User(
            role="Teacher",
            name="Mr. Joe",
            email = "mrjoe@mrjoe.com",
            password = "fakies",
            admin=False
        ),
        User(
            role="Scientist",
            name="fakie scientist",
            email = "science@science.com",
            password = "fakies",
            admin=False
        )
    ]
    for user in users:
        db.session.add(user)
    db.session.commit()
    classrooms = [
        Group(
            user_id=users[1].id,
            name="first classroom",
            school_district="the district",
            city="Philadelphia",
            state="PA", 
            country="US",
            time_zone="US/Eastern",
            monday_start_time="09:00",
            scientist_preferred_type="cool ones"
        )
    ]
    for classroom in classrooms:
        db.session.add(classroom)
    db.session.commit()

if __name__ == '__main__':
    cli()
