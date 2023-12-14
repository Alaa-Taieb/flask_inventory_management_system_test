from flask_app import app , check_login
from flask import render_template , session , url_for , redirect , request


@app.route('/products')
@check_login
def products():

    return render_template("products.html")