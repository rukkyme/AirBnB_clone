#!/usr/bin/python3
"""File storage module"""
import json


class FileStorage:
    """serializes instances to a JSON file and
    deserializes JSON file to instances"""

    __file_path = "file.json"
    __objects = {}

    def all(self):
        """returns the dictionary __objects"""
        return self.__objects

    def new(self, obj):
        """sets in __objects the obj with key
        <obj class name>.id"""
        key = f"{obj.__class__.__name__}.{obj.id}"
        self.__objects[key] = obj

    def save(self):
        """ serializes __objects to the JSON file
        (path: __file_path)"""
        objects = {key: obj.to_dict() for key, obj in self.__objects.items()}
        with open(self.__file_path, 'w') as f:
            json.dump(objects, f)

    def reload(self):
        """deserializes the JSON file to __objects"""
        from models.base_model import BaseModel
        from models.user import User
        from models.state import State
        from models.city import City
        from models.amenity import Amenity
        from models.place import Place
        from models.review import Review
        classmap = {"BaseModel": BaseModel,
                    "User": User,
                    "State": State,
                    "City": City,
                    "Amenity": Amenity,
                    "Place": Place,
                    "Review": Review}

        try:
            with open(self.__file_path) as f:
                objects = json.load(f)

            for objdict in objects.values():
                class_string = objdict["__class__"]
                clsname = classmap[class_string]
                if clsname:
                    obj = clsname(**objdict)
                    self.new(obj)
            # Alternative method using eval(removed due to unsafe nature)
            # for key, objdict in objects.items():
            #    classname = objdict["__class__"]
            #    print(classname)
            #    obj = eval("{}({})".format(classname, "**objdict"))
            #    self.new(obj)
        except (FileNotFoundError):
            pass
