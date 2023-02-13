#!/usr/bin/python3
from models.base_model import BaseModel
"""contains User class"""


class User(BaseModel):
    """class User that inherits from BaseModel"""
    email = ""
    password = ""
    first_name = ""
    last_name = ""
