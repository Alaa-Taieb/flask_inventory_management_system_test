from flask_app import app , check_login
from flask import render_template , session , url_for , redirect , request , flash
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
    if result:
        
        messages_object = {'category': "error" , 'messages': ["Reference Check [Invalid]: A product with this reference exists in the database."]}
        return {'ref_validity': False , 'messages_object': messages_object}
    else:
        print(data['reference'])
        messages_object = {'category': "success" , 'messages': [f"Reference Check [Valid]: {data['reference']} is a Valid reference."]}
        return {'ref_validity': True, 'messages_object': messages_object}