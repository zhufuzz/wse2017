from flask_script import Manager
from app import app
from models import User

manager = Manager(app)

# python manage.py save
@manager.command
def save():
    user = User(1, 'jikexueyuan')
    user.save()

# python manage.py query_all
@manager.command
def query_all():
    users = User.query_all()
    for u in users:
        print u


if __name__ == "__main__":
    manager.run()