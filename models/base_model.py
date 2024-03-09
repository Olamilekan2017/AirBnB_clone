#!/usr/bin/python3
"""BaseModel class for the AirBnB project"""
import uuid
from datetime import datetime
import models


class BaseModel:
    """Representing the BaseModel of the AirBnB project"""

    def __init__(self, *args, **kwargs):
        """Initializing BaseModel class
        Args: *args: not used
        **kwargs (dict): attributes of key/value pairs"""
        datefmt = "%Y-%m-%dT%H:%M:%S.%f"
        self.id = str(uuid.uuid4())
        self.created_at = datetime.today()
        self.updated_at = datetime.today()
        if kwargs:
            for key, val in kwargs.items():
                if key in ["created_at", "updated_at"]:
                    self.__dict__[key] = datetime.strptime(val, datefmt)
                else:
                    self.__dict__[key] = val
        else:
            models.storage.new(self)

    def __str__(self):
        """Gets and returns string representation of BaseModel"""
        classnm = self.__class__.__name__
        return "[{}] ({}) {}".format(classnm, self.id, self.__dict__)

    def save(self):
        """Updating with the recent datetime and save"""
        self.updated_at = datetime.today()
        models.storage.save()

    def to_dict(self):
        """Generating the dicts representation of BaseModel instance"""
        repdict = self.__dict__.copy()
        repdict["created_at"] = self.created_at.isoformat()
        repdict["updated_at"] = self.updated_at.isoformat()
        repdict["__class__"] = type(self).__name__
        return repdict
