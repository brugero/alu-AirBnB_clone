#!/usr/bin/python3
"""Unit tests for BaseModel class"""
import unittest
from datetime import datetime
from models.base_model import BaseModel
from models import storage
import os
import uuid

class TestBaseModel(unittest.TestCase):
    """Test cases for BaseModel class"""

    def setUp(self):
        """Set up test environment"""
        self.model = BaseModel()
        self.file_path = "file.json"
        try:
            os.remove(self.file_path)
        except FileNotFoundError:
            pass
        storage.all().clear()

    def tearDown(self):
        """Clean up test environment"""
        try:
            os.remove(self.file_path)
        except FileNotFoundError:
            pass
        storage.all().clear()

    def test_init_no_kwargs(self):
        """Test initialization without kwargs"""
        self.assertIsInstance(self.model.id, str)
        self.assertIsInstance(self.model.created_at, datetime)
        self.assertIsInstance(self.model.updated_at, datetime)
        self.assertEqual(self.model.created_at, self.model.updated_at)

    def test_init_with_kwargs(self):
        """Test initialization with kwargs"""
        dict_data = {
            "id": str(uuid.uuid4()),
            "created_at": datetime.now().isoformat(),
            "updated_at": datetime.now().isoformat(),
            "name": "Test Model",
            "__class__": "BaseModel"
        }
        model = BaseModel(**dict_data)
        self.assertEqual(model.id, dict_data["id"])
        self.assertEqual(model.name, "Test Model")
        self.assertIsInstance(model.created_at, datetime)
        self.assertIsInstance(model.updated_at, datetime)
        self.assertNotIn("__class__", model.__dict__)

    def test_str(self):
        """Test string representation"""
        str_rep = str(self.model)
        expected = f"[BaseModel] ({self.model.id}) {self.model.__dict__}"
        self.assertEqual(str_rep, expected)

    def test_save(self):
        """Test save method updates updated_at and saves to storage"""
        old_updated_at = self.model.updated_at
        self.model.save()
        self.assertNotEqual(old_updated_at, self.model.updated_at)
        self.assertTrue(os.path.exists(self.file_path))
        with open(self.file_path, 'r') as f:
            content = f.read()
            self.assertIn(f"BaseModel.{self.model.id}", content)

    def test_to_dict(self):
        """Test to_dict method"""
        self.model.name = "Test Model"
        self.model.number = 42
        model_dict = self.model.to_dict()
        self.assertEqual(model_dict["__class__"], "BaseModel")
        self.assertEqual(model_dict["id"], self.model.id)
        self.assertEqual(model_dict["name"], "Test Model")
        self.assertEqual(model_dict["number"], 42)
        self.assertEqual(model_dict["created_at"], self.model.created_at.isoformat())
        self.assertEqual(model_dict["updated_at"], self.model.updated_at.isoformat())

    def test_unique_id(self):
        """Test that each instance has a unique ID"""
        model2 = BaseModel()
        self.assertNotEqual(self.model.id, model2.id)

    def test_datetime_timezone(self):
        """Test that created_at and updated_at are timezone naive"""
        self.assertIsNone(self.model.created_at.tzinfo)
        self.assertIsNone(self.model.updated_at.tzinfo)

if __name__ == '__main__':
    unittest.main()