from flask_script import Manager
from app import app
import sqlite3
from models import User

manager = Manager(app)

#python manage.py hello
@manager.command
def hello():
    print "hello world!!!"

#python manage.py hello_world -m jikexueyuan
@manager.option('-m', '--msg', dest='msg_val', default='world')
def hello_world(msg_val):
    print "hello" + msg_val
    
#python manage.py init_db
@manager.command
def init_db():
    sql = 'create table user (id INT, name TEXT)'
    conn = sqlite3.connect("test.db")
    cursor = conn.cursor()
    cursor.execute(sql)
    conn.commit()
    cursor.close()
    conn.close()

#python manage.py save
@manager.command
def save():
    user = User(2, 'jikexueyuan')
    user.save()

#python manage.py query_all
@manager.command
def query_all():
    users = User.query()
    for user in users:
        print user


if __name__ == "__main__":
    manager.run()