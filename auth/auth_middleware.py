from functools import wraps
from flask import request, Response
import configparser

# Load basic auth credentials
auth_config = configparser.ConfigParser()
auth_config.read('/etc/haproxy-configurator/auth/auth.cfg')
BASIC_AUTH_USERNAME = auth_config.get('auth', 'username')
BASIC_AUTH_PASSWORD = auth_config.get('auth', 'password')

def check_auth(username, password):
    return username == BASIC_AUTH_USERNAME and password == BASIC_AUTH_PASSWORD

def authenticate():
    return Response(
        'Authentication required.', 401,
        {'WWW-Authenticate': 'Basic realm="Login Required"'}
    )

def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if not auth or not check_auth(auth.username, auth.password):
            return authenticate()
        return f(*args, **kwargs)
    return decorated

def setup_auth(app):
    """Setup authentication for the Flask app"""
    # This function can be used to register auth-related configurations
    # if needed in the future
    pass
