from flask.ext.bootstrap import Bootstrap
from flask import Flask, render_template
app = Flask(__name__)
bootstrap = Bootstrap(app)

@app.route('/')
def index():
    name = 'kingname'
    return render_template('template2.html', name=name)

if __name__ == "__main__":
    app.run(debug=True)
