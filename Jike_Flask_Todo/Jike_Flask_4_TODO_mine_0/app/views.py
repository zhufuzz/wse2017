from app import app
from flask import render_template
#from models import Todo, TodoForm
#from datetime import datetime


@app.route('/')
def index():
    #form = TodoForm()
    #todos = Todo.objects.order_by('-time')
    return render_template("index.html")