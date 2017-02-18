from flask import Flask
from flask import render_template
from flask import redirect
from flask import url_for
from flask import request

app=Flask(__name__)

@app.route('/')
def index():
	return redirect(url_for('add'))

@app.route('/add',methods=['GET','POST'])
def add():
	if request.method =="POST":
		a=request.form['adder1']
		b=request.form['adder2']
		a=int(a)
		b=int(b)
		sum=a+b
		return render_template('index.html',adder1=str(a),adder2=str(b),message=str(sum))
	return render_template('index.html')

if __name__=='__main__':
	app.run(port=8080)