from flask_app import app
from flask import request


@app.route('/utils/host')
def get_host():
    """
    The function `get_host` returns the IP address of the server.
    :return: A dictionary with a key 'host' and the value of the request.host.
    """
    return {'host':request.host}



