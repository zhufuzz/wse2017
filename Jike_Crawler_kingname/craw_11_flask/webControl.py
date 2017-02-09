#--coding:utf8--
from flask.ext.bootstrap import Bootstrap
from flask import Flask, render_template
from flask.ext.wtf import Form
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import Required

app = Flask(__name__)
bootstrap = Bootstrap(app)

app. config['SECRET_KEY'] = 'youcouldneverknowhis-name'
app.config.from_object(__name__)

class contentForm(Form):
    commandInConfig = StringField(u'内置命令')
    commandInWrite = TextAreaField(u'写入Python代码', default=u"写入Python代码")
    userName = StringField(u'用户名', validators=[Required()])
    password = StringField(u'密码', validators=[Required()])
    sendCommand = SubmitField(u'发送命令' )
    clearCommand = SubmitField(u'清空命令')

@app.route('/', methods=['GET'])
def index():
    form = contentForm()
    return render_template('index.html', form=form)

if __name__ == "__main__":
    app.run(debug=True)