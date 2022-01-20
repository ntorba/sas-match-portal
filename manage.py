from flask.cli import FlaskGroup

from flask_app.app import create_app, db 
from flask_app.models import ClassRoom, User 

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
            name="fakie teacher",
            email = "hello@hello.com",
            password = "fakies",
            admin=False
        ),
        User(
            role="Scientist",
            name="fakie scientist",
            email = "science@hello.com",
            password = "fakies",
            admin=False
        )
    ]
    classrooms = [
        ClassRoom(
            user_id=1,
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
    for user in users:
        db.session.add(user)
    for classroom in classrooms:
        db.session.add(classroom)
    db.session.commit()

if __name__ == '__main__':
    cli()
