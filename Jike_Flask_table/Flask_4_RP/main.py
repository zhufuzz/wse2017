from flask import Flask
from flask import request
from flask import render_template
from flask import redirect
from model import *
app=Flask(__name__)

from wtforms import Form,TextField,PasswordField,validators

class LoginForm(Form):
	username = TextField("username",[validators.Required()])
	password = PasswordField("password",[validators.Required()])


@app.route("/register",methods=['GET','POST'])
def register():
	myForm=LoginForm(request.form)
	if request.method=='POST':
		u=User(myForm.username.data,myForm.password.data)
		u.add()
		return redirect("http://www.jikexueyuan.com")
	return render_template('index.html',form=myForm)

@app.route("/login",methods=['GET','POST'])
def login():
	myForm=LoginForm(request.form)
	if request.method =='POST':
		u=User(myForm.username.data,myForm.password.data)
		if (u.isExisted()):
			return redirect("http://www.jikexueyuan.com")
		else:
			return "Login Failed"
	return render_template('index.html',form=myForm)

@app.route("/search",methods=['GET','POST'])
def search():
	if request.method=='POST':
		uname=request.form['username']
		u=User.query.filter_by(username=uname).first()
		l=[]
		l=Item.query.filter_by(sender_id=u.id).all()
		return render_template("search.html",context=l)
	return render_template("search.html")

if __name__=="__main__":
	app.run(port=8080,debug=True)