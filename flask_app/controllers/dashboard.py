from flask_app import app

from flask_app import check_login

@app.route('/dashboard')
@check_login
def dashboard():

    return "Hello you are in the dashboard."