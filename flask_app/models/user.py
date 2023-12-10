from flask_app.config.mysqlconnection import connectToMySQL, DB
from flask_app import app
from flask_bcrypt import Bcrypt
from flask import flash
from flask_app.models.role import Role

bcrypt = Bcrypt(app) # Initialize bcrypt object for password hashing

class User:
    """
    This class represents a User object in the application.
    It includes methods for getting, creating, updating, and deleting users.
    It also includes methods for validating login and registration data.
    """
    def __init__(self , data):
        """
        Initializes the User object with data from a dictionary.

        Args:
            data: A dictionary containing user information.
        """
        self.id = data['id']
        self.username = data['username']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

        self.role = None # Initialize role attribute as None (will be populated later)


    # Get all
    @classmethod
    def get_all(cls):
        """
        Retrieves all users from the database and returns them as a list of User objects.
        Also associates each user with their corresponding role.

        Returns:
            A list of User objects.
        """
        query = "SELECT * FROM user JOIN role ON role.id = user.role_id;"
        results = connectToMySQL(DB).query_db(query)

        # Create an empty list to store users
        users = []

        # Check if any results were returned
        if results:
            # Iterate over each row and populate the users list
            for row in results:
                user = cls(row)

                # Create a Role object from the role data and associate it with the user
                role_data = {
                    "id": row['role.id'],
                    "role_name": row['role_name'],
                    "description": row['description'],
                    "created_at": row['role.created_at'],
                    "updated_at": row['role.updated_at'],
                }
                user.role = Role(role_data)
                users.append(user)
        return users
    
    # Class method to get a specific user by ID
    @classmethod
    def get_by_id(cls , data):
        """
        Retrieves a specific user from the database based on its ID.
        Also associates the user with their corresponding role.

        Args:
            data: A dictionary containing the "id" key with the desired user ID.

        Returns:
            A User object or None if no user is found.
        """
        query = "SELECT * FROM user WHERE id = %(id)s;"
        results = connectToMySQL(DB).query_db(query , data)

        # Initialize a variable to store the user
        user = None

        # Check if a result was found
        if results:
            user = cls(results[0])

            # Create a Role object from the role data and associate it with the user
            role_data = {
                "id": results[0]['role.id'],
                "role_name": results[0]['role_name'],
                "description": results[0]['description'],
                "created_at": results[0]['role.created_at'],
                "updated_at": results[0]['role.updated_at'],
            }
            user.role = Role(role_data)
        return user
    
    # Class method to get a user by username
    @classmethod
    def get_by_username(cls, data):
        """
        Retrieves a specific user from the database based on their username.

        Args:
            data: A dictionary containing the "username" key.

        Returns:
            A User object or None if no user is found.
        """

        query = "SELECT * FROM user WHERE username = %(username)s;"
        results = connectToMySQL(DB).query_db(query, data)

        # Initialize a variable to store the user
        user = None

        # Check if a result was found
        if results:
            user = cls(results[0])

        return user

    
    # Class method to register a new user
    @classmethod
    def register(cls, data):
        """
        Registers a new user in the database by hashing their password and inserting
        data into the user table.

        Args:
            data: A dictionary containing user information, including username, password, and role_id.

        Returns:
            The ID of the newly inserted user or None if the registration fails.
        """

        # Hash the password using bcrypt
        hashed_password = bcrypt.generate_password_hash(data["password"])

        # Update the data dictionary with the hashed password
        data = dict(data)
        data["password"] = hashed_password

        # Prepare the SQL query for insertion into the user table
        query = "INSERT INTO user (username, password, role_id) VALUES (%(username)s, %(password)s, %(role_id)s);"

        # Execute the query and return the ID of the inserted user
        return connectToMySQL(DB).query_db(query, data)
    
    # Class method to update user data
    @classmethod
    def update(cls, data):
        """
        Updates a user's information in the database, including their password if provided.

        Args:
            data: A dictionary containing user information and potentially the updated password.

        Returns:
            True if the update was successful, False otherwise.
        """

        # Check if password is updated
        if "password" in data:
            # Hash the new password
            hashed_password = bcrypt.generate_password_hash(data["password"])
            data["password"] = hashed_password

        # Update the user data in the database
        query = "UPDATE user SET username = %(username)s, password = %(password)s, role_id = %(role_id)s WHERE id = %(id)s;"
        return connectToMySQL(DB).query_db(query, data)
    

    # Method to delete a user
    def delete(cls, data):
        """
        Deletes a user from the database based on their ID.

        Args:
            data: A dictionary containing the "id" key with the user ID to delete.

        Returns:
            True if the deletion was successful, False otherwise.
        """

        query = "DELETE FROM user WHERE id = %(id)s;"
        return connectToMySQL(DB).query_db(query, data)
    
    # Static method to validate login credentials
    @staticmethod
    def validate_login(data):
        """
        Validates user login credentials by checking if the username exists and the password matches.

        Args:
            data: A dictionary containing username and password.

        Returns:
            True if the login credentials are valid, False otherwise.
        """

        is_valid = True

        # Check if username exists
        user_in_db = User.get_by_username(data)
        if not user_in_db:
            flash(f"No user with username [{data['username']}] exists in our database.", "login_error")
            is_valid = False

        # Check if password matches
        elif not bcrypt.check_password_hash(user_in_db.password, data["password"]):
            flash("Wrong password.", "login_error")
            is_valid = False

        return is_valid
    
    # Static method to validate user registration data
    @staticmethod
    def validate_register(data):
        """
        Validates user registration data by checking if the username is already taken and if the passwords match.

        Args:
            data: A dictionary containing user registration information.

        Returns:
            True if the registration data is valid, False otherwise.
        """

        is_valid = True

        # Check if username is already taken
        user_in_db = User.get_by_username(data)
        if user_in_db:
            flash(f"User already exists with username [{data['username']}]", "register_error")
            is_valid = False

        # Check if passwords match
        if data["password"] != data["confirm_password"]:
            flash("Passwords don't match.", "register_error")
            is_valid = False

        return is_valid
    

    

