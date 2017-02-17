from app import db
import datetime
#from flask.ext.mongoengine.wtf import model_form

class Todo(db.Document):
    content = db.StringField()
    time = db.DateTimeField(default = datetime.datetime.now())
    status = db.IntField(default = 0)


#TodoForm = model_form(Todo)

