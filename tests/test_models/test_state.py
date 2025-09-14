#!/usr/bin/python3
"""Unit tests for State class"""
import unittest
from datetime import datetime
from models.state import State
from models import storage
import os

class TestState(unittest.TestCase):
    """Test cases for State class"""

    def setUp(self):
        """Set up test environment"""
        self.state = State()
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
        self.assertEqual(self.state.name, "")
        self.assertIsInstance(self.state.id, str)
        self.assertIsInstance(self.state.created_at, datetime)
        self.assertIsInstance(self.state.updated_at, datetime)

    def test_init_with_kwargs(self):
        """Test initialization with kwargs"""
        dict_data = {
            "id": "123e4567-e89b-12d3-a456-426614174000",
            "created_at": datetime.now().isoformat(),
            "updated_at": datetime.now().isoformat(),
            "name": "California",
            "__class__": "State"
        }
        state = State(**dict_data)
        self.assertEqual(state.name, "California")
        self.assertIsInstance(state.created_at, datetime)

    def test_str(self):
        """Test string representation"""
        self.state.name = "California"
        str_rep = str(self.state)
        expected = f"[State] ({self.state.id}) {self.state.__dict__}"
        self.assertEqual(str_rep, expected)

    def test_save(self):
        """Test save method"""
        old_updated_at = self.state.updated_at
        self.state.save()
        self.assertNotEqual(old_updated_at, self.state.updated_at)
        self.assertTrue(os.path.exists(self.file_path))

    def test_to_dict(self):
        """Test to_dict method"""
        self.state.name = "California"
        state_dict = self.state.to_dict()
        self.assertEqual(state_dict["__class__"], "State")
        self.assertEqual(state_dict["name"], "California")
        self.assertEqual(state_dict["id"], self.state.id)

if __name__ == '__main__':
    unittest.main()