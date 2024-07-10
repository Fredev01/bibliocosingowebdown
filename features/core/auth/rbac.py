from enum import Enum
from functools import wraps

from flask_jwt_extended import get_current_user, verify_jwt_in_request
from flask_jwt_extended.exceptions import NoAuthorizationError

from flaskr import jwt
from flaskr.models import UserModel


# here define callback function which returns current user model
@jwt.user_lookup_loader
def user_lookup_callback(_jwt_header, jwt_data):
    """ callback for fetching authenticated user from db """
    identity = jwt_data["sub"]
    return UserModel.query.filter_by(username=identity).one_or_none()

# @check_access decorator function
def check_access(roles: [Enum] = []):
    def decorator(f):
        @wraps(f)
        def decorator_function(*args, **kwargs):
            # calling @jwt_required()
            verify_jwt_in_request()
            # fetching current user from db
            current_user: UserModel = get_current_user()
            # checking user role
            if current_user.role not in roles:
                raise NoAuthorizationError("Role is not allowed.")
            return f(*args, **kwargs)
        return decorator_function
    return decorator

