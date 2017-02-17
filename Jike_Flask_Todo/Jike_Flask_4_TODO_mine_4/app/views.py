from app import app
from flask import render_template, request
from models import Todo#, TodoForm
#from datetime import datetime


@app.route('/')
def index():
    #form = TodoForm()
    todos = Todo.objects.all()
    return render_template("index.html", todos=todos)



@app.route('/add', methods=['POST',])
def add():
    form = TodoForm(request.form)
    content = form['content']
    todo = Todo(content=content)
    todo.save()
    todos = Todo.objects.all()
    return render_template("index.html",todos=todos)