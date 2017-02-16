
#coding:utf-8

from flask.ext.restful import reqparse, Resource
from JsonObject import JsonObject
from model import User
auth=reqparse.RequestParser()

class Authentication(Resource):
	def get(self):
		pass
	def post(self):
		auth.add_argument('username',required=True,help="Username is Required")
		auth.add_argument('password',required=True,help="Password is Required")
		args=auth.parse_args()
		username = args['username']
		password = args['password']
		u = User(username,password)
		jsobj = JsonObject()
		if u.isExisted():
			jsobj.put("code",1)
			jsobj.put("desc","User Existed")
		else:
			jsobj.put("code",2)
			jsobj.put("desc","User Not Existed")
		return jsobj.getJson(),200