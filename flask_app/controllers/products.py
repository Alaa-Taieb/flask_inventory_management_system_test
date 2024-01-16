from flask_app import app , check_login , admin_required
from flask import render_template , session , url_for , redirect , request , flash , jsonify
from ast import literal_eval
from flask_app.models.product import Product



@app.route('/products')
@check_login
def products():

    return render_template("products.html")

@app.route('/products/check_reference', methods=['post'])
@check_login
def check_reference():
    """
    The function `check_reference` checks if a product with a given reference exists in the database and
    returns a validity status along with a messages object.
    :return: The function `check_reference()` returns a dictionary with two keys: 'ref_validity' and
    'messages_object'. The value of 'ref_validity' is a boolean indicating whether the reference is
    valid or not. The value of 'messages_object' is a dictionary with two keys: 'category' and
    'messages'. The value of 'category' is a string indicating the category of the message (
    """
    data = request.form
    result = Product.get_by_reference(data)
    print(result)
    if result:
        
        messages_object = {'category': "error" , 'messages': ["Reference Check [Invalid]: A product with this reference exists in the database."]}
        return {'ref_validity': False , 'messages_object': messages_object}
    else:
        print(data['reference'])
        messages_object = {'category': "success" , 'messages': [f"Reference Check [Valid]: {data['reference']} is a Valid reference."]}
        return {'ref_validity': True, 'messages_object': messages_object}
    
@app.route('/products/create', methods=['POST'])
@check_login
@admin_required
def create_product():
    """
    The function creates a product based on the provided data and returns a message object indicating
    the success or failure of the operation.
    :return: the `message_object`.
    """
    data = request.form
    message_object = Product.validate_create(data)
    if message_object["category"] == 'success':
        print("*"*50)
        print("Product Would have been created!")
        print("Product Data: ")
        print(data)
        print("*"*50)

        Product.create(data)
    return message_object

@app.route('/products/get_all_paginated' , methods={"POST"})
@check_login
def get_products_paginated():
    """
    The function `get_products_paginated` retrieves a paginated list of products based on the provided
    page number and number of rows per page.
    :return: a dictionary with a key 'products' and the value is the result of calling the
    'get_all_pagination' method on the 'Product' class.
    """
    data_request_object = request.data
    data_request_object = literal_eval(data_request_object.decode())
    print(data_request_object)
    
    pagination_return_object = Product.get_all_pagination(data_request_object)
    products_page = pagination_return_object['products_page']

    
    products_page_dict = Product.list_object_to_dict(products_page , data_request_object['desired_results_format'])

    return {'products': products_page_dict , 'number_of_pages': pagination_return_object['number_of_pages']}