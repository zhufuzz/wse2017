#--coding:utf8--
from flask.ext.bootstrap import Bootstrap
from flask import Flask, render_template, redirect
from flask.ext.wtf import Form
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired
from util.DataBaseManager import DataBaseManager

app = Flask(__name__)
bootstrap = Bootstrap(app)

app. config['SECRET_KEY'] = 'youcouldneverknowhis-name'
app.config.from_object(__name__)

class contentForm(Form):
    commandInConfig = StringField(u'内置命令')
    commandInWrite = TextAreaField(u'写入Python代码', default=u"写入Python代码")
    userName = StringField(u'用户名', validators=[DataRequired()])
    password = StringField(u'密码', validators=[DataRequired()])
    sendCommand = SubmitField(u'发送命令' )
    clearCommand = SubmitField(u'清空命令')

@app.route('/', methods=['GET', 'POST'])
def index():
    form = contentForm()
    dataBaseManager = DataBaseManager()

    if form.validate_on_submit():

        innerCommand = form.commandInConfig.data
        writeCommand = form.commandInWrite.data
        userName = form.userName.data
        password = form.password.data
        info = {'innerCommand': innerCommand, 'writeCommand': writeCommand,
                'userName': userName, 'password': password}
        dataBaseManager.insert(info)
        return redirect('/')
    return render_template('index.html', form=form)

if __name__ == "__main__":
    app.run(debug=True)