from flask import Flask
from flask_app.config.global_variables import SECRET_KEY , LOGGED_USER_ID_SESSION_KEY , LOGGED_USER_ROLE_ID_SESSION_KEY
from functools import wraps
from flask import session , redirect , url_for


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
    return LOGGED_USER_ID_SESSION_KEY in session

def authenticate(user_id = None , username = None):
    """
    The `authenticate` function logs a user into a session based on their user ID or username.
    
    :param user_id: The user_id parameter is used to authenticate a user based on their unique user ID.
    If a user with the specified user ID is found, their ID and role ID are stored in the session, and a
    message is printed indicating that the user has been logged in. If no user is found with the
    :param username: The username parameter is used to authenticate a user based on their username
    :return: The function will return True if the user is successfully authenticated and logged in
    session. If the user is not authenticated or there is an error, it will return False.
    """
    from flask_app.models.user import User

    user = None
    if user_id:
        user = User.get_by_id({'id': user_id})
        session[LOGGED_USER_ID_SESSION_KEY] = user.id
        session[LOGGED_USER_ROLE_ID_SESSION_KEY] = user.role.id
        print("User Logged in session.")
        return True
    elif username:
        user = User.get_by_username({'username': username})
        session[LOGGED_USER_ID_SESSION_KEY] = user.id
        session[LOGGED_USER_ROLE_ID_SESSION_KEY] = user.role.id
        print("User Logged in session.")
        return True    
    print("Unable to log user in session.")
    
    return False

def check_login(func):
    """
    The `check_login` function is a decorator that checks if a user is authenticated before allowing
    them to access a certain function.
    
    :param func: The `func` parameter is a function that will be decorated with the `check_login`
    decorator
    :return: The function `decorated_function` is being returned.
    """
    @wraps(func)
    def decorated_function(*args , **kwargs):
        if not authenticated():
            return redirect(url_for('index'))
        return func(*args , **kwargs)
    return decorated_function