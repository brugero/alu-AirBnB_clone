#!/usr/bin/python3
"""Unit tests for FileStorage class"""
import unittest
import os
import json
from models.engine.file_storage import FileStorage
from models.base_model import BaseModel
from models.user import User
from models import storage

class TestFileStorage(unittest.TestCase):
    """Test cases for FileStorage class"""

    def setUp(self):
        """Set up test environment"""
        self.storage = FileStorage()
        self.file_path = "file.json"
        try:
            os.remove(self.file_path)
        except FileNotFoundError:
            pass
        FileStorage._FileStorage__objects = {}

    def tearDown(self):
        """Clean up test environment"""
        try:
            os.remove(self.file_path)
        except FileNotFoundError:
            pass
        FileStorage._FileStorage__objects = {}

    def test_all(self):
        """Test all method returns dictionary"""
        self.assertIsInstance(self.storage.all(), dict)
        self.assertEqual(self.storage.all(), {})

    def test_new(self):
        """Test new method adds object to storage"""
        model = BaseModel()
        self.storage.new(model)
        key = f"BaseModel.{model.id}"
        self.assertIn(key, self.storage.all())
        self.assertEqual(self.storage.all()[key], model)

    def test_save(self):
        """Test save method serializes objects to JSON file"""
        model = BaseModel()
        model.name = "Test Model"
        self.storage.new(model)
        self.storage.save()
        self.assertTrue(os.path.exists(self.file_path))
        with open(self.file_path, 'r') as f:
            data = json.load(f)
            key = f"BaseModel.{model.id}"
            self.assertIn(key, data)
            self.assertEqual(data[key]["name"], "Test Model")

    def test_reload(self):
        """Test reload method deserializes JSON file to objects"""
        model = BaseModel()
        model.name = "Test Model"
        self.storage.new(model)
        self.storage.save()
        self.storage.all().clear()
        self.storage.reload()
        key = f"BaseModel.{model.id}"
        self.assertIn(key, self.storage.all())
        self.assertEqual(self.storage.all()[key].name, "Test Model")
        self.assertIsInstance(self.storage.all()[key], BaseModel)

    def test_reload_no_file(self):
        """Test reload with no file does not raise exception"""
        try:
            self.storage.reload()
            self.assertEqual(self.storage.all(), {})
        except Exception:
            self.fail("reload() raised an unexpected exception")

    def test_reload_user(self):
        """Test reload with User class"""
        user = User()
        user.email = "test@example.com"
        self.storage.new(user)
        self.storage.save()
        self.storage.all().clear()
        self.storage.reload()
        key = f"User.{user.id}"
        self.assertIn(key, self.storage.all())
        self.assertEqual(self.storage.all()[key].email, "test@example.com")
        self.assertIsInstance(self.storage.all()[key], User)

if __name__ == '__main__':
    unittest.main()