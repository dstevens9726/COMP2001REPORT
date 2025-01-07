from functools import wraps
from flask import request, jsonify, session

SECRET_KEY = "UserCookie"

def is_user_logged_in():
    
    return 'email' in session  #check if user in session by email

def get_user_data():

    if is_user_logged_in():
        return {'email': session['email'], 'role': session['role']} #if in session return role
    return None

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        user_data = get_user_data()
        if not user_data:
            return {'message': 'User is not logged in'}, 401
        request.user_data = user_data
        return f(*args, **kwargs)
    return decorated

def role_required(role):
    def wrapper(f):
        @wraps(f)
        def decorated(*args, **kwargs):
            user_data = getattr(request, 'user_data', None)
            if not user_data or user_data.get('role') != role:
                return {'message': 'Unauthorized user, insufficient role'}, 403
            return f(*args, **kwargs)
        return decorated
    return wrapper
