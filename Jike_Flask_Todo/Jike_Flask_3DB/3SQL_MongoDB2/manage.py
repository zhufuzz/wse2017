from flask_script import Manager
from app import app
from models import User

manager = Manager(app)

@manager.command
def save():
    # user = User('jike', 'jike@jikexueyuan.com')
    # user.save()
    user = User(name = 'jike02', email = 'jike02@jikexueyuan.com')

@manager.command
def query_all():
    # users = User.query_user()
    # for user in users:
    #     print user
	users = User.objects.all()
	for user in users:
		print user

if __name__ == "__main__":
    manager.run()