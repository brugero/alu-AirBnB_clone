#!/usr/bin/python3
"""BaseModel module for AirBnB clone project"""
from uuid import uuid4
from datetime import datetime

class BaseModel:
    """Base class for all AirBnB objects"""
    
    def __init__(self, *args, **kwargs):
        """Initialize a new BaseModel instance
        
        Args:
            *args: Variable length argument list (not used)
            **kwargs: Keyword arguments for initialization
        """
        from models import storage  # Import inside method
        if kwargs:
            for key, value in kwargs.items():
                if key != '__class__':
                    if key in ['created_at', 'updated_at']:
                        value = datetime.fromisoformat(value)
                    setattr(self, key, value)
        else:
            self.id = str(uuid4())
            self.created_at = datetime.now()
            self.updated_at = datetime.now()
            storage.new(self)

    def __str__(self):
        """Return string representation of the instance"""
        return f"[{self.__class__.__name__}] ({self.id}) {self.__dict__}"

    def save(self):
        """Update updated_at with current datetime and save to storage"""
        from models import storage  # Import inside method
        self.updated_at = datetime.now()
        storage.save()

    def to_dict(self):
        """Return dictionary representation of the instance"""
        result = self.__dict__.copy()
        result['__class__'] = self.__class__.__name__
        result['created_at'] = self.created_at.isoformat()
        result['updated_at'] = self.updated_at.isoformat()
        return result