from flask import render_template

from datawire.core import app

app.template_folder = '../templates'

@app.route("/")
def index():
    return render_template('index.html')
