#!/usr/bin/python3
"""BaseModel module"""
import uuid
from datetime import datetime
from models import storage


class BaseModel:
    """defines all common attributes/methods
    for other classes"""

    def __init__(self, *args, **kwargs):
        """Initialise new instances"""
        if kwargs:
            for key, value in kwargs.items():
                if key != '__class__':
                    if key == 'created_at':
                        value = datetime.fromisoformat(value)
                        setattr(self, key, value)
                        continue
                    if key == 'updated_at':
                        value = datetime.fromisoformat(value)
                        setattr(self, key, value)
                        continue
                    setattr(self, key, value)
        else:
            self.id = str(uuid.uuid4())
            self.created_at = datetime.today()
            self.updated_at = datetime.today()
            storage.new(self)

    def __str__(self):
        """Return object in string format"""
        return f"[{self.__class__.__name__}] ({self.id}) {self.__dict__}"

    def save(self):
        """Save objects"""
        self.updated_at = datetime.today()
        storage.save()

    def to_dict(self):
        """convert object to dict"""
        objdict = dict(self.__dict__)
        objdict['id'] = self.id
        objdict['created_at'] = self.created_at.isoformat()
        objdict['updated_at'] = self.updated_at.isoformat()
        objdict['__class__'] = self.__class__.__name__
        return objdict
