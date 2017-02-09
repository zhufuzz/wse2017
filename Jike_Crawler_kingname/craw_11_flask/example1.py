#--coding:utf8--
from flask import Flask, render_template
app = Flask(__name__)

@app.route("/")
def hello():
    return u'hello world'

@app.route("/jikexueyuan")
def jikexueyuan():
    return u'极客学院的同学大家好~'

@app.route("/jikexueyuan/<name>")
def jikexxx(name):
    return name + u': 你好啊~'

@app.route("/page/<pages>")
def page(pages):
    return u'这是第' + pages + u'页'

@app.route("/page/<pages>/total/<total>")
def totalPage(pages, total):
    return u'第' + pages + u',共' + total + u'页'

@app.route("/templa")
def testTemp():
    title = u'测试模板'
    name = 'kingname'
    pages = {'page': '10', 'total': '20'}
    return render_template('template1.html', title=title, name=name, pages=pages)

if __name__ == "__main__":
    app.run(debug=True)