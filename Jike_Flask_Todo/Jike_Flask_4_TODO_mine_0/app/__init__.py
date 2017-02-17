from flask import Flask

app = Flask(__name__)

from app import views, models
# 这个时候他们两个都是空的