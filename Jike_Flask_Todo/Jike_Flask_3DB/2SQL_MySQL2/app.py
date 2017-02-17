from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import sqlite3
import os

app = Flask(__name__)
# sqlite3.connect(os.path.abspath("user.db"))
app.config['SQLALCHEMY_DAYABASE_URI'] = "mysql://root:dashizi@localhost:3306/jikexueyuan"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = "True"
db = SQLAlchemy(app)

@app.route('/')
def hello_world():
    return 'Hello World!'

if __name__ == '__main__':
    app.run()

# jdbc:mysql: // localhost:3306