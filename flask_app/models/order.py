from flask_app.config.mysqlconnection import connectToMySQL , DB
from flask_app.models.user import User
from flask_app.models.product import Product
from flask_app.models.order_item import OrderItem


class Order:
    """
    This class represents an order in the application.
    It includes methods for getting, creating, updating, and deleting orders.
    """

    def __init__(self, data):
        """
        Initializes the Order object with data from a dictionary.

        Args:
            data: A dictionary containing order information.
        """

        self.id = data["id"]  # Unique identifier of the order
        self.created_at = data["created_at"]  # Date and time the order was created
        self.updated_at = data["updated_at"]  # Date and time the order was last updated

        self.user = None  # User who placed the order (initially None, populated later)
        self.order_items = []  # List of order items associated with the order (initially empty)

    @classmethod
    def get_all(cls):
        """
        Gets all orders from the database along with associated order items, products, and user who placed the order.

        Returns:
            A list of Order objects containing complete information.
        """

        query = """
            SELECT * FROM order
            LEFT JOIN user ON user.id = order.user_id
            LEFT JOIN order_item ON order_item.order_id = order.id
            LEFT JOIN product ON order_item.product_id = product.id
        """

        results = connectToMySQL(DB).query_db(query)

        orders = []

        if results:
            for row in results:
                new_order = True

                user_data = {
                    "id": row["user.id"],
                    "username": row["username"],
                    "password": row["password"],
                    "created_at": row["user.created_at"],
                    "updated_at": row["user.updated_at"],
                }

                order_item_data = {
                    "id": row["order_item.id"],
                    "quantity": row["quantity"],
                    "created_at": row["order_item.created_at"],
                    "updated_at": row["order_item.updated_at"],
                }

                product_data = {
                    "id": row["product.id"],
                    "name": row["name"],
                    "price": row["price"],
                    "reference": row["reference"],
                    "created_at": row["product.created_at"],
                    "updated_at": row["product.updated_at"],
                }

                number_of_orders = len(orders)

                if number_of_orders > 0:
                    old_order = orders[len(orders) - 1]

                    if old_order.id == row["id"]:
                        new_order = False

                        order_item = OrderItem(order_item_data)
                        order_item.product = Product(product_data)
                        old_order.order_items.append(order_item)

                if new_order:
                    order = cls(row)
                    order.user = User(user_data)
                    order_item = OrderItem(order_item_data)
                    order_item.product = Product(product_data)
                    order.order_items.append(order_item)
                    orders.append(order)

        return orders

    @classmethod
    def get_by_id(cls, data):
        """
        Retrieves a specific order from the database based on its ID.

        Args:
            data: A dictionary containing the order ID as "id" key.

        Returns:
            An Order object with complete information if found, None otherwise.
        """

        query = """
            SELECT * FROM order
            LEFT JOIN user ON user.id = order.user_id
            LEFT JOIN order_item ON order_item.order_id = order.id
            LEFT JOIN product ON order_item.product_id = product.id
            WHERE id = %(id)s;
        """

        results = connectToMySQL(DB).query_db(query, data)

        order = None

        if results:
            order = Order(results[0])
            user_data = {
                "id": results[0]["user.id"],
                "username": results[0]["username"],
                "password": results[0]["password"],
                "created_at": results[0]["user.created_at"],
                "updated_at": results[0]["user.updated_at"],
            }
            order.user = User(user_data)

            for row in results:
                order_item_data = {
                    "id": row["order_item.id"],
                    "quantity": row["quantity"],
                    "created_at": row["order_item.created_at"],
                    "updated_at": row["order_item.updated_at"],
                }

                product_data = {
                    "id": row["product.id"],
                    "name": row["name"],
                    "price": row["price"],
                    "reference": row["reference"],
                    "created_at": row["product.created_at"],
                    "updated_at": row["product.updated_at"],
                }

                order_item = OrderItem(order_item_data)
                order_item.product = Product(product_data)
                order.order_items.append(order_item)

        return order
        

    @classmethod
    def create(cls, data):
        """
        Creates a new order in the database.

        Args:
            data: A dictionary containing the user ID as "user_id" key.

        Returns:
            The ID of the newly created order if successful.
        """

        query = "INSERT INTO order (user_id) VALUES(%(user_id)s);"
        return connectToMySQL(DB).query_db(query, data)

        
    
    @classmethod
    def delete(cls, data):
        """
        Deletes an existing order from the database.

        Args:
            data: A dictionary containing the order ID as "id" key.

        Returns:
            True if the deletion was successful.
        """
        query = "DELETE FROM order WHERE id = %(id)s;"
        return connectToMySQL(DB).query_db(query , data)
    