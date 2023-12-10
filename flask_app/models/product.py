from flask_app.config.mysqlconnection import connectToMySQL , DB

class Product:
    """
    This class represents a product in the application.
    It includes methods for getting, creating, updating, and deleting products.
    """

    def __init__(self, data):
        """
        Initializes the product object with data from a dictionary.

        Args:
            data: A dictionary containing product information.
        """

        self.id = data["id"]
        self.name = data["name"]
        self.price = data["price"]
        self.reference = data["reference"]
        self.created_at = data["created_at"]
        self.updated_at = data["updated_at"]


    # Class method to get all products
    @classmethod
    def get_all(cls):
        """
        Retrieves all products from the database and returns them as a list of Product objects.

        Returns:
            A list of Product objects.
        """

        query = "SELECT * FROM product;"
        results = connectToMySQL(DB).query_db(query)

        products = []

        # Check if any results were returned
        if results:
            # Iterate over each row and create a product object for each
            for row in results:
                products.append(cls(row))

        return products
    
    # Class method to get a product by ID
    @classmethod
    def get_by_id(cls, data):
        """
        Retrieves a specific product from the database based on its ID.

        Args:
            data: A dictionary containing the "id" key with the desired product ID.

        Returns:
            A Product object or None if no product is found.
        """

        query = "SELECT * FROM product WHERE id = %(id)s;"
        results = connectToMySQL(DB).query_db(query, data)

        product = None

        # Check if a result was found
        if results:
            product = cls(results[0])

        return product
    
    # Class method to create a new product
    @classmethod
    def create(cls, data):
        """
        Creates a new product in the database.

        Args:
            data: A dictionary containing product information.

        Returns:
            The ID of the newly created product.
        """

        query = "INSERT INTO product (name, price, reference) VALUES (%(name)s, %(price)s, %(reference)s);"
        return connectToMySQL(DB).query_db(query, data)
    
    # Class method to update an existing product
    @classmethod
    def update(cls, data):
        """
        Updates an existing product in the database with new information.

        Args:
            data: A dictionary containing product information and the ID.

        Returns:
            True if the update was successful, False otherwise.
        """

        query = "UPDATE product SET name = %(name)s, price = %(price)s, reference = %(reference)s WHERE id = %(id)s;"
        return connectToMySQL(DB).query_db(query, data)
    
    # Class method to delete a product
    @classmethod
    def delete(cls, data):
        """
        Deletes a product from the database based on its ID.

        Args:
            data: A dictionary containing the "id" key with the product ID to delete.

        Returns:
            True if the deletion was successful, False otherwise.
        """

        query = "DELETE FROM product WHERE id = %(id)s;"
        return connectToMySQL(DB).query_db(query, data)