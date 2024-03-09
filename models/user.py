#!/usr/bin/python3
"""Class named User has been derived from the BaseMOdel class"""
from models.base_model import BaseModel


class User(BaseModel):
    """Representing the User class from BaseModel
    Attributes: email (str): users email
    password (str): users password
    first_name (str): users first name
    last_name (str): users last name"""
    email = ""
    password = ""
    first_name = ""
    last_name = ""
