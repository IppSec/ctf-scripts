from pydantic import BaseModel, validator, constr, ValidationError
from urllib.error import HTTPError

class NameModel(BaseModel):
    username: constr(min_length=1, max_length=256)  # Adjust the max length as needed

    @validator('username')
    def validate_name(cls, username):
        # Check if the name contains only alphanumeric characters and apostrophes        
        if not all(char.isalnum() or char == " " or char == "'" or char == "-" for char in username):
            raise ValueError('Name must contain only letters, numbers, and apostrophes')
        return username