from flask_script import Manager
from app import app
from models import User

manager = Manager(app)

@manager.command
def save():
    user = User(1, 'jikexueyuan01')
    user.save()


@manager.command
def query_all():
    pass


if __name__ == "__main__":
    manager.run()