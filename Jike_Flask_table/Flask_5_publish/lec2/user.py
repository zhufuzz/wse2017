from flask import Blueprint
from model import User

user=Blueprint('user',__name__)

@user.route('/<int:userid>')
def showUser(userid):
	u = User.query.filter_by(id=userid).first()
	return u.getUsername()