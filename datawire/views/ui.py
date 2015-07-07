from flask import render_template

from datawire.core import app


@app.route('/lists/<path:id>')
@app.route('/lists')
@app.route('/')
def ui(**kwargs):
    return render_template("layout.html")
