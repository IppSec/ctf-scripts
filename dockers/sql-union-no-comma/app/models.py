from pydantic import BaseModel, validator, constr, ValidationError
from urllib.error import HTTPError
import re

class NameModel(BaseModel):
    username: constr(min_length=1, max_length=256)  # Adjust the max length as needed

    @validator('username')
    def validate_name(cls, username):
        # Check if the name contains only alphanumeric characters and apostrophes        
        if not re.match(r'^[a-zA-Z0-9()*\' -]+$', username):            
            raise ValueError('Name must contain only letters, numbers, and apostrophes')
        return username