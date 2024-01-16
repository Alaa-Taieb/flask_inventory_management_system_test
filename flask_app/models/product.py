from flask_app.config.mysqlconnection import connectToMySQL , DB
from math import ceil

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
    
    @classmethod
    def get_by_reference(cls, data):
        """
        The function `get_by_reference` retrieves a product from a database based on its reference
        number.
        
        :param cls: The parameter "cls" is a reference to the class that is calling the method. It is
        used to create an instance of the class using the data retrieved from the database
        :param data: The `data` parameter is a dictionary that contains the reference value that will be
        used in the SQL query. The dictionary should have a key called "reference" with the
        corresponding reference value as its value
        :return: The method `get_by_reference` returns an instance of the `cls` class if a product with
        the given reference is found in the database. If no product is found, it returns `None`.
        """
        query = "SELECT * FROM product WHERE reference = %(reference)s;"
        results = connectToMySQL(DB).query_db(query , data)

        if results:
            product = cls(results[0])
            return product
        return None
    
    @classmethod
    def get_all_pagination(cls , data):
        """
        The function `get_all_pagination` takes in a class and data, retrieves all products from the
        database, and returns a specific page of products based on the given page number and number of
        rows per page.
        
        :param cls: The parameter `cls` is typically used as a reference to the class itself. It is
        commonly used in class methods to access class-level variables or methods. In this case, it
        seems that `cls` is a reference to the class that contains the `get_all_pagination` method
        :param data: The `data` parameter is a dictionary that contains information about the
        pagination. It should have the following keys:
        :return: a list of products that correspond to a specific page number and number of rows per
        page.
        """
        # Data will contain information to create a product but also information about pagination
        # For pagination we would need to know the page number and the number of rows in each page.
        # data = {... , 'page_number': value , 'rows_per_page': value}

        # Here we get all the products from the database
        products = cls.get_all()

        # Calculate the start and end index
        start_index = data['page_number']*data['rows_per_page']
        end_index = start_index + data['rows_per_page']

        # Create a new list taking values from the products list
        products_page = products[start_index: end_index]

        # Calculate the number of pages using the rows_per_page value
        number_of_pages = ceil(len(products) / data['rows_per_page'])

        return {'products_page':products_page , 'number_of_pages': number_of_pages}

    @staticmethod
    def validate_create(data):
        """
        The function `validate_create` checks if the product name is at least 3 characters long and if
        the product price is greater than 0, and returns a message object indicating the validation
        result.
        
        :param data: The `data` parameter is a dictionary that contains information about a product. It
        should have the following keys:
        :return: The function `validate_create` returns a dictionary object `message_object` which
        contains the category of the validation result ('success' or 'error') and a list of messages.
        """
        message_object = {'category': 'success' , 'messages': []}
        # Check if name is more than 2 characters long.
        # Check if price is more than 0
        if len(data['name']) < 3:
            message_object["category"] = 'error'
            message_object["messages"].append('Product data check [Invalid]: Product name is less than 3 characters.')
        if float(data['price']) < 0:
            message_object["category"] = 'error'
            message_object["messages"].append('Product data check [Invalid]: Product price must be greater than 0.')

        if message_object['category'] == 'success':
            message_object["messages"].append('Product data check [Valid]: Product saved successfully.')
        return message_object
    
    @staticmethod
    def list_object_to_dict(list , desired_results_format):
        """
        The function converts a list of objects into a list of dictionaries.
        
        :param list: The parameter "list" is a list of objects that you want to convert to a list of
        dictionaries. Each object in the list should have attributes that can be accessed using dot
        notation
        :return: a new list where each item in the original list is converted to a dictionary.
        """

        new_list = []
        for item in list:
            data = dict(item)
            desired_format_object = {}
            for key, value in desired_results_format.items():
                desired_format_object[value] = data[key]
            new_list.append(desired_format_object)


        

        
        return new_list

    def __iter__(self):
        """
        The function is an iterator that yields key-value pairs for the id, name, price, reference,
        created_at, and updated_at attributes.
        """
        yield 'id', self.id
        yield 'name', self.name
        yield 'price', self.price
        yield 'reference', self.reference
        yield 'created_at', self.created_at
        yield 'updated_at', self.updated_at

    
