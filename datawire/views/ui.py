from flask import render_template

from datawire.core import app


@app.route('/<path:id>')
@app.route('/')
def ui(**kwargs):
    return render_template("layout.html")
