#!/usr/bin/python3
"""Class named Review has been derived from the BaseModel class"""
from models.base_model import BaseModel


class Review(BaseModel):
    """Representing the Review class from BaseModel
    Attributes: place_id (str): place id
    user_id (str): user id
    text (str): review text"""
    place_id = ""
    user_id = ""
    text = ""
