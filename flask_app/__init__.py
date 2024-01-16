from flask import Flask
from flask_app.config.global_variables import SECRET_KEY , LOGGED_USER_ID_SESSION_KEY , LOGGED_USER_ROLE_ID_SESSION_KEY
from functools import wraps
from flask import session , redirect , url_for
from flask_app.models.role import Role


# Create a Flask application instance
app = Flask(__name__)




# Set the secret key for session management
app.secret_key = SECRET_KEY

# The line `app.config['JSON_SORT_KEYS'] = False` is setting a configuration option for the Flask
# application.
app.config['JSON_SORT_KEYS'] = False


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

def admin_required(func):
    """
    The `admin_required` function is a decorator that checks if the user has the role of an admin before
    allowing access to a function.
    
    :param func: The `func` parameter is a function that will be decorated with the `admin_required`
    decorator. This function will be called when the decorated function is invoked
    :return: The function `decorated_function` is being returned.
    """

    @wraps(func)
    def decorated_function(*args , **kwargs):
        """
        The above function is a decorator that checks if the logged-in user has the 'admin' role and
        returns an error message if they don't have permission.
        :return: The function `decorated_function` is being returned.
        """
        
        if not get_role_name(session[LOGGED_USER_ROLE_ID_SESSION_KEY]) == 'admin':
            # Return redirect will apparently not work because we disabled default and so we need to return a message_object or something else that will be handled on the client side by JavaScript.
            return {'category': 'error' , 'messages':["You don't have permission!"]}
        return func(*args , **kwargs)
    return decorated_function

def get_role_name(id):
    """
    The function `get_role_name` retrieves the role name associated with a given ID, or returns False if
    no role is found.
    
    :param id: The `id` parameter is the unique identifier of the role that we want to retrieve the name
    for
    :return: the role name if a role with the given id exists, otherwise it returns False.
    """
    role = Role.get_by_id({'id': id})
    if role:
        return role.role_name
    return False


def clear_authentication_data():
    """
    The function clears the authentication data stored in the session.
    """
    session.pop(LOGGED_USER_ID_SESSION_KEY)
    session.pop(LOGGED_USER_ROLE_ID_SESSION_KEY)
    

