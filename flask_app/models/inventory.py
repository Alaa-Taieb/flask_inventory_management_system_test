from flask_app.config.mysqlconnection import connectToMySQL , DB
from flask_app.models.product import Product


class Inventory:
    """
    This class represents an inventory item in the application.
    It includes methods for getting, creating, updating, and deleting inventory items.
    """

    def __init__(self, data):
        """
        Initializes the Inventory object with data from a dictionary.

        Args:
            data: A dictionary containing inventory information.
        """

        self.id = data["id"]
        self.quantity = data["quantity"]
        self.created_at = data["created_at"]
        self.updated_at = data["updated_at"]

        self.product = None  # Initialize product attribute as None (will be populated later)


    # Class method to get all inventory with their associated products
    @classmethod
    def get_all(cls, data):
        """
        Retrieves all inventory items from the database and returns them as a list of Inventory objects.
        Also associates each inventory item with its corresponding product.

        Returns:
            A list of Inventory objects.
        """

        query = "SELECT * FROM inventory JOIN product ON inventory.product_id = product.id;"
        results = connectToMySQL(DB).query_db(query, data)

        inventories = []

        if results:
            # Iterate over each row and create an Inventory object
            for row in results:
                inventory = cls(row)

                # Create a Product object from the product data and associate it with the inventory item
                product_data = {
                    "id": row["product.id"],
                    "name": row["name"],
                    "price": row["price"],
                    "reference": row["reference"],
                    "created_at": row["product.created_at"],
                    "updated_at": row["product.updated_at"],
                }

                inventory.product = Product(product_data)
                inventories.append(inventory)

        return inventories
    
    # Class method to get an inventory item by ID
    @classmethod
    def get_by_id(cls, data):
        """
        Retrieves a specific inventory item from the database based on its ID.
        Also associates the inventory item with its corresponding product.

        Args:
            data: A dictionary containing the "id" key with the desired inventory item ID.

        Returns:
            An Inventory object or None if no inventory item is found.
        """

        query = "SELECT * FROM inventory JOIN product ON product.id = inventory.product_id WHERE id = %(id)s;"
        results = connectToMySQL(DB).query_db(query, data)

        inventory = None

        if results:
            inventory = cls(results[0])

            # Create a Product object from the product data and associate it with the inventory item
            product_data = {
                "id": results[0]["product.id"],
                "name": results[0]["name"],
                "price": results[0]["price"],
                "reference": results[0]["reference"],
                "created_at": results[0]["product.created_at"],
                "updated_at": results[0]["product.updated_at"],
            }

            inventory.product = Product(product_data)

        return inventory
    
    # Class method to create a new inventory item
    @classmethod
    def create(cls, data):
        """
        Creates a new inventory item in the database.

        Args:
            data: A dictionary containing inventory information.

        Returns:
            The ID of the newly created inventory item.
        """

        query = "INSERT INTO inventory (quantity, product_id) VALUES (%(quantity)s, %(product_id)s);"
        return connectToMySQL(DB).query_db(query, data)
    

    # Method to update an existing inventory item
    def update(cls, data):
        """
        Updates an existing inventory item in the database with new information.

        Args:
            data: A dictionary containing updated inventory information and the ID.

        Returns:
            True if the update was successful, False otherwise.
        """

        query = "UPDATE inventory SET quantity = %(quantity)s, product_id = %(product_id)s WHERE id = %(id)s;"
        return connectToMySQL(DB).query_db(query, data)
    

    # Method to delete an inventory item
    def delete(cls, data):
        """
        Deletes an inventory item from the database based on its ID.

        Args:
            data: A dictionary containing the "id" key with the inventory item ID to delete.

        Returns:
            True if the deletion was successful, False otherwise.
        """

        query = "DELETE FROM inventory WHERE id = %(id)s;"
        return connectToMySQL(DB).query_db(query, data)
