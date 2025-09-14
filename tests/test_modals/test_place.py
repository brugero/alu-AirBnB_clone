#!/usr/bin/python3
"""Unit tests for Place class"""
import unittest
from datetime import datetime
from models.place import Place
from models import storage
import os

class TestPlace(unittest.TestCase):
    """Test cases for Place class"""

    def setUp(self):
        """Set up test environment"""
        self.place = Place()
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
        self.assertEqual(self.place.city_id, "")
        self.assertEqual(self.place.user_id, "")
        self.assertEqual(self.place.name, "")
        self.assertEqual(self.place.description, "")
        self.assertEqual(self.place.number_rooms, 0)
        self.assertEqual(self.place.number_bathrooms, 0)
        self.assertEqual(self.place.max_guest, 0)
        self.assertEqual(self.place.price_by_night, 0)
        self.assertEqual(self.place.latitude, 0.0)
        self.assertEqual(self.place.longitude, 0.0)
        self.assertEqual(self.place.amenity_ids, [])
        self.assertIsInstance(self.place.id, str)
        self.assertIsInstance(self.place.created_at, datetime)
        self.assertIsInstance(self.place.updated_at, datetime)

    def test_init_with_kwargs(self):
        """Test initialization with kwargs"""
        dict_data = {
            "id": "123e4567-e89b-12d3-a456-426614174000",
            "created_at": datetime.now().isoformat(),
            "updated_at": datetime.now().isoformat(),
            "city_id": "city-123",
            "user_id": "user-123",
            "name": "Cozy Apartment",
            "description": "A nice place",
            "number_rooms": 2,
            "number_bathrooms": 1,
            "max_guest": 4,
            "price_by_night": 100,
            "latitude": 37.7749,
            "longitude": -122.4194,
            "amenity_ids": ["amenity-1", "amenity-2"],
            "__class__": "Place"
        }
        place = Place(**dict_data)
        self.assertEqual(place.city_id, "city-123")
        self.assertEqual(place.user_id, "user-123")
        self.assertEqual(place.name, "Cozy Apartment")
        self.assertEqual(place.description, "A nice place")
        self.assertEqual(place.number_rooms, 2)
        self.assertEqual(place.number_bathrooms, 1)
        self.assertEqual(place.max_guest, 4)
        self.assertEqual(place.price_by_night, 100)
        self.assertEqual(place.latitude, 37.7749)
        self.assertEqual(place.longitude, -122.4194)
        self.assertEqual(place.amenity_ids, ["amenity-1", "amenity-2"])

    def test_str(self):
        """Test string representation"""
        self.place.name = "Cozy Apartment"
        str_rep = str(self.place)
        expected = f"[Place] ({self.place.id}) {self.place.__dict__}"
        self.assertEqual(str_rep, expected)

    def test_save(self):
        """Test save method"""
        old_updated_at = self.place.updated_at
        self.place.save()
        self.assertNotEqual(old_updated_at, self.place.updated_at)
        self.assertTrue(os.path.exists(self.file_path))

    def test_to_dict(self):
        """Test to_dict method"""
        self.place.name = "Cozy Apartment"
        self.place.number_rooms = 2
        place_dict = self.place.to_dict()
        self.assertEqual(place_dict["__class__"], "Place")
        self.assertEqual(place_dict["name"], "Cozy Apartment")
        self.assertEqual(place_dict["number_rooms"], 2)
        self.assertEqual(place_dict["id"], self.place.id)

if __name__ == '__main__':
    unittest.main()