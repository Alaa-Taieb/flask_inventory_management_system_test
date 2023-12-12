from flask_app import app
from flask import render_template
from flask_app import check_login

@app.route('/dashboard')
@check_login
def dashboard():

    return render_template("dashboard.html")