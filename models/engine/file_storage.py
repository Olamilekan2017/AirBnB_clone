#!/usr/bin/python3
"""FileStorage class of AirBnB project"""
import json
from datetime import datetime
from models.base_model import BaseModel
from models.user import User
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.place import Place
from models.review import Review


class FileStorage:
    """Representing the FileStorage for the AirBnB project
    Private Class Attributes:
    __file_path (str): file name designated to save objects
    __objects (dict): dict that contains instance of objects"""
    __file_path = "file.json"
    __objects = {}

    def all(self):
        """Returns the dictionary of __objects"""
        return FileStorage.__objects

    def new(self, obj):
        """Sets in __objects the obj with key <obj class name>.id"""
        key = "{}.{}".format(obj.__class__.__name__, obj.id)
        FileStorage.__objects[key] = obj

    def save(self):
        """Serializes __objects to the JSON file"""
        dictobj = FileStorage.__objects
        serobj = {obj: dictobj[obj].to_dict() for obj in dictobj.keys()}
        with open(FileStorage.__file_path, "w") as f:
            json.dump(serobj, f)

    def reload(self):
        """Deserializes the JSON file to __objects"""
        try:
            with open(FileStorage.__file_path) as f:
                serobj = json.load(f)
                for sobjdt in serobj.values():
                    classnm = sobjdt["__class__"]
                    del sobjdt["__class__"]
                    self.new(eval(classnm)(**sobjdt))
        except FileNotFoundError:
            return
