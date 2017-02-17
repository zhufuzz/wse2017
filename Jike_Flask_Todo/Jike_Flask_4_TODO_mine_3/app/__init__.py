from flask import Flask
from flask.ext.mongoengine import MongoEngine

app = Flask(__name__)

db = MongoEngine(app)

from app import views, models