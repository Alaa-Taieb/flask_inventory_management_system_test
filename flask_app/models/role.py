from flask_app.config.mysqlconnection import connectToMySQL , DB


class Role:
    """
    This class represents a Role object in the application.
    It includes methods for getting, creating, updating, and deleting roles.
    """
    def __init__(self , data):
        """
        Initializes the Role object with data from a dictionary.

        Args:
            data: A dictionary containing role information.
        """
        self.id = data['id']
        self.role_name = data['role_name']
        self.description = data['description']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']


    # Class method to get all roles
    @classmethod 
    def get_all(cls):
        """
        Retrieves all roles from the database and returns them as a list of Role objects.

        Returns:
            A list of Role objects.
        """

        query = "SELECT * FROM role;"
        results = connectToMySQL(DB).query_db(query)

        # Create an empty list to store role instances
        roles = []

        # Check if any results were returned
        if results:
            # Iterate over each row and populate the list
            for row in results:
                roles.append(cls(row))

        return roles

    
    # Class method to get a specific role by ID
    @classmethod
    def get_by_id(cls, data):
        """
        Retrieves a specific role from the database based on its ID.

        Args:
            data: A dictionary containing the "id" key with the desired role ID.

        Returns:
            A Role object or None if no role is found.
        """

        query = "SELECT * FROM role WHERE id = %(id)s;"
        results = connectToMySQL(DB).query_db(query, data)

        # Initialize a variable to store the role
        role = None

        # Check if a result was found
        if results:
            # Create a Role object from the first result
            role = cls(results[0])

        return role
    
    # Class method to create a new role
    @classmethod
    def create(cls, data):
        """
        Creates a new role in the database based on provided data.

        Args:
            data: A dictionary containing "role_name" and "description" keys.

        Returns:
            The ID of the newly created role or None if unsuccessful.
        """

        query = "INSERT INTO role (role_name, description) VALUES (%(role_name)s, %(description)s);"
        return connectToMySQL(DB).query_db(query, data)
    
    # Class method to update an existing role
    @classmethod
    def update(cls, data):
        """
        Updates an existing role in the database based on provided data.

        Args:
            data: A dictionary containing "id", "role_name", and "description" keys.

        Returns:
            True if the update was successful, False otherwise.
        """

        query = "UPDATE role SET role_name = %(role_name)s, description = %(description)s WHERE id = %(id)s;"
        return connectToMySQL(DB).query_db(query, data)
    
    # Class method to delete a role
    @classmethod
    def delete(cls, data):
        """
        Deletes a role from the database based on its ID.

        Args:
            data: A dictionary containing the "id" key with the role ID to delete.

        Returns:
            True if the deletion was successful, False otherwise.
        """

        query = "DELETE FROM role WHERE id = %(id)s;"
        return connectToMySQL(DB).query_db(query, data)

    