from flask_app import app
from flask import render_template, redirect, session, request
from flask_app import authenticated
from flask_app.models.user import User

@app.route("/")
def index():
    """
    Renders the index template.
    """
    return render_template("index.html")

@app.route("/login", methods=["POST"])
def login():
    """
    Handles user login and redirects based on success or failure.

    **Preconditions:**
    * Authenticated user is redirected to the dashboard.

    **Steps:**
    1. Check if user is already authenticated.
    2. Extract user data from the request form.
    3. Validate user login credentials.
    4. If login is successful:
        * Store user ID in session.
        * Redirect to the dashboard.
    5. If login fails:
        * Redirect to the index page.
    """
    if authenticated():
        return redirect("/dashboard")

    data = request.form

    # Decide which user data to save in session (e.g., role_name, username, user ID)

    if User.validate_login(data):
        session["user_id"] = User.get_by_username().id
        return redirect("/dashboard")

    return redirect("/")