#coding:utf-8
from flask import Flask
from flask.ext.restful import Api
from userAPI import *

app = Flask(__name__)
api = Api(app)

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

api.add_resource(Authentication,'/auth')

if __name__=='__main__':
	app.run(port=8080)