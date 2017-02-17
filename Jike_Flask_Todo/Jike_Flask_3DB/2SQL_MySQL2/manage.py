from flask_script import Manager
from app import app, db
from models import User



manager = Manager(app)

@manager.command

# python manage.py save
def save():
	#db.create_all()
	# user = User(1, 'jikexueyuan01')
    # user.save()
	user = User(2, 'jikexueyuan02')
	db.session.add(user)
	db.session.commit()


# python manage.py query_all
@manager.command
def query_all():
	#db.create_all()
	users = User.query.all()
	for u in users:
		print u

if __name__ == "__main__":
	db.create_all()
	# init.db()
	manager.run()