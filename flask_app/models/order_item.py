from flask_app.config.mysqlconnection import connectToMySQL, DB


class OrderItem:
    """
    This class represents an order item in the application.
    It includes methods for creating, updating, and deleting order items.
    """

    def __init__(self, data):
        """
        Initializes the order item object with data from a dictionary.

        Args:
            data: A dictionary containing order item information.
        """

        self.id = data["id"]
        self.quantity = data["quantity"]
        self.created_at = data["created_at"]
        self.updated_at = data["updated_at"]

        self.product = None  # Initialize product attribute as None (will be populated later)

    # Class method to create a new order item
    @classmethod
    def create(cls, data):
        """
        Creates a new order item in the database.

        Args:
            data: A dictionary containing order item information.

        Returns:
            The ID of the newly created order item.
        """

        query = "INSERT INTO order_item (quantity, product_id, order_id) VALUES (%(quantity)s, %(product_id)s, %(order_id)s);"
        return connectToMySQL(DB).query_db(query, data)

    # Class method to update an existing order item
    @classmethod
    def update(cls, data):
        """
        Updates an existing order item in the database with new information.

        Args:
            data: A dictionary containing updated order item information and the ID.

        Returns:
            True if the update was successful, False otherwise.
        """

        query = "UPDATE order_item SET quantity = %(quantity)s, product_id = %(product_id)s, order_id = %(order_id)s WHERE id = %(id)s;"
        return connectToMySQL(DB).query_db(query, data)

    # Class method to delete an order item
    @classmethod
    def delete(cls, data):
        """
        Deletes an order item from the database based on its ID.

        Args:
            data: A dictionary containing the "id" key with the order item ID to delete.

        Returns:
            True if the deletion was successful, False otherwise.
        """

        query = "DELETE FROM order_item WHERE id = %(id)s;"
        return connectToMySQL(DB).query_db(query, data)
