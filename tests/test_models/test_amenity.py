#!/usr/bin/python3
"""Unit tests for Amenity class"""
import unittest
from datetime import datetime
from models.amenity import Amenity
from models import storage
import os

class TestAmenity(unittest.TestCase):
    """Test cases for Amenity class"""

    def setUp(self):
        """Set up test environment"""
        self.amenity = Amenity()
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
        self.assertEqual(self.amenity.name, "")
        self.assertIsInstance(self.amenity.id, str)
        self.assertIsInstance(self.amenity.created_at, datetime)
        self.assertIsInstance(self.amenity.updated_at, datetime)

    def test_init_with_kwargs(self):
        """Test initialization with kwargs"""
        dict_data = {
            "id": "123e4567-e89b-12d3-a456-426614174000",
            "created_at": datetime.now().isoformat(),
            "updated_at": datetime.now().isoformat(),
            "name": "WiFi",
            "__class__": "Amenity"
        }
        amenity = Amenity(**dict_data)
        self.assertEqual(amenity.name, "WiFi")
        self.assertIsInstance(amenity.created_at, datetime)

    def test_str(self):
        """Test string representation"""
        self.amenity.name = "WiFi"
        str_rep = str(self.amenity)
        expected = f"[Amenity] ({self.amenity.id}) {self.amenity.__dict__}"
        self.assertEqual(str_rep, expected)

    def test_save(self):
        """Test save method"""
        old_updated_at = self.amenity.updated_at
        self.amenity.save()
        self.assertNotEqual(old_updated_at, self.amenity.updated_at)
        self.assertTrue(os.path.exists(self.file_path))

    def test_to_dict(self):
        """Test to_dict method"""
        self.amenity.name = "WiFi"
        amenity_dict = self.amenity.to_dict()
        self.assertEqual(amenity_dict["__class__"], "Amenity")
        self.assertEqual(amenity_dict["name"], "WiFi")
        self.assertEqual(amenity_dict["id"], self.amenity.id)

if __name__ == '__main__':
    unittest.main()