from flask import Flask
from flask_app.config.global_variables import SECRET_KEY
from flask import session


# Create a Flask application instance
app = Flask(__name__)


# Set the secret key for session management
app.secret_key = SECRET_KEY


# Define a custom function to check if a user is authenticated
def authenticated():
    """
    Checks whether a user is currently logged in based on the presence
    of a 'user_id' key in the session.

    Returns:
        True if a user is authenticated, False otherwise.
    """
    return 'user_id' in session
