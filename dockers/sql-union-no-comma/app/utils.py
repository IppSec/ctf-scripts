from pydantic import ValidationError
from models import NameModel
from functools import wraps

def validate_username(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        # Validate the username parameter
        try:
            query = NameModel(username=kwargs['username']).dict()
        except ValidationError as e:
            return str(e), 400

        kwargs['query'] = query
        return func(*args, **kwargs)
    return wrapper