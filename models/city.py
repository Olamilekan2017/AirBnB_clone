#!/usr/bin/python3
"""Class named City has been derived from BaseModel class"""
from models.base_model import BaseModel


class City(BaseModel):
    """Representing the City class from BaseModel class
    Attributes: state_id (str): state id
    name (str): name of the city"""
    state_id = ""
    name = ""
