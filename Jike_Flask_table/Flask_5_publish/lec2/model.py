# model.py
from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root@localhost/test'
db = SQLAlchemy(app)

class User(db.Model):
	id = db.Column(db.Integer,primary_key=True)
	username = db.Column(db.String(32),unique=True)
	password = db.Column(db.String(32))
	def __init__(self,username,password):
		self.username = username
		self.password = password
	def add(self):
		try:
			db.session.add(self)
			db.session.commit()
			return self.id
		except Exception,e:
			db.session.rollback()
			return e
		finally:
			return 0
	def isExisted(self):
		temUser=User.query.filter_by(username=self.username,password=self.password).first()
		if temUser is None:
			return 0
		else:
			return 1
	def getUsername(self):
		return self.username

class Item(db.Model):
	id=db.Column(db.Integer,primary_key=True)
	context=db.Column(db.String(128))
	sender_id=db.Column(db.Integer)
	def __init__(self,context,sender_id):
		self.context=context
		self.sender_id=sender_id
	def add(self):
		try:
			db.session.add(self)
			db.session.commit()
			return self.id
		except Exception,e:
			db.session.rollback()
			return e
		finally:
			return 0

class UIRelation(db.Model):
	id=db.Column(db.Integer,primary_key=True)
	uid=db.Column(db.Integer)
	iid=db.Column(db.Integer)