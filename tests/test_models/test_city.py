#!/usr/bin/python3
"""Unit tests for City class"""
import unittest
from datetime import datetime
from models.city import City
from models import storage
import os

class TestCity(unittest.TestCase):
    """Test cases for City class"""

    def setUp(self):
        """Set up test environment"""
        self.city = City()
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

    def test_attributes(self):
        """Test default attributes"""
        self.assertEqual(self.city.state_id, "")
        self.assertEqual(self.city.name, "")
        self.assertIsInstance(self.city.id, str)
        self.assertIsInstance(self.city.created_at, datetime)
        self.assertIsInstance(self.city.updated_at, datetime)

    def test_init_with_kwargs(self):
        """Test initialization with kwargs"""
        dict_data = {
            "id": "123e4567-e89b-12d3-a456-426614174000",
            "created_at": datetime.now().isoformat(),
            "updated_at": datetime.now().isoformat(),
            "state_id": "state-123",
            "name": "San Francisco",
            "__class__": "City"
        }
        city = City(**dict_data)
        self.assertEqual(city.state_id, "state-123")
        self.assertEqual(city.name, "San Francisco")
        self.assertIsInstance(city.created_at, datetime)

    def test_str(self):
        """Test string representation"""
        self.city.name = "San Francisco"
        str_rep = str(self.city)
        expected = f"[City] ({self.city.id}) {self.city.__dict__}"
        self.assertEqual(str_rep, expected)

    def test_save(self):
        """Test save method"""
        old_updated_at = self.city.updated_at
        self.city.save()
        self.assertNotEqual(old_updated_at, self.city.updated_at)
        self.assertTrue(os.path.exists(self.file_path))

    def test_to_dict(self):
        """Test to_dict method"""
        self.city.state_id = "state-123"
        self.city.name = "San Francisco"
        city_dict = self.city.to_dict()
        self.assertEqual(city_dict["__class__"], "City")
        self.assertEqual(city_dict["state_id"], "state-123")
        self.assertEqual(city_dict["name"], "San Francisco")
        self.assertEqual(city_dict["id"], self.city.id)

if __name__ == '__main__':
    unittest.main()