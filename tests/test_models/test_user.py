#!/usr/bin/python3
"""Unit tests for User class"""
import unittest
from datetime import datetime
from models.user import User
from models import storage
import os

class TestUser(unittest.TestCase):
    """Test cases for User class"""

    def setUp(self):
        """Set up test environment"""
        self.user = User()
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
        self.assertEqual(self.user.email, "")
        self.assertEqual(self.user.password, "")
        self.assertEqual(self.user.first_name, "")
        self.assertEqual(self.user.last_name, "")
        self.assertIsInstance(self.user.id, str)
        self.assertIsInstance(self.user.created_at, datetime)
        self.assertIsInstance(self.user.updated_at, datetime)

    def test_init_with_kwargs(self):
        """Test initialization with kwargs"""
        dict_data = {
            "id": "123e4567-e89b-12d3-a456-426614174000",
            "created_at": datetime.now().isoformat(),
            "updated_at": datetime.now().isoformat(),
            "email": "test@example.com",
            "password": "secret",
            "first_name": "John",
            "last_name": "Doe",
            "__class__": "User"
        }
        user = User(**dict_data)
        self.assertEqual(user.email, "test@example.com")
        self.assertEqual(user.password, "secret")
        self.assertEqual(user.first_name, "John")
        self.assertEqual(user.last_name, "Doe")
        self.assertIsInstance(user.created_at, datetime)

    def test_str(self):
        """Test string representation"""
        self.user.email = "test@example.com"
        str_rep = str(self.user)
        expected = f"[User] ({self.user.id}) {self.user.__dict__}"
        self.assertEqual(str_rep, expected)

    def test_save(self):
        """Test save method"""
        old_updated_at = self.user.updated_at
        self.user.save()
        self.assertNotEqual(old_updated_at, self.user.updated_at)
        self.assertTrue(os.path.exists(self.file_path))

    def test_to_dict(self):
        """Test to_dict method"""
        self.user.email = "test@example.com"
        self.user.first_name = "John"
        user_dict = self.user.to_dict()
        self.assertEqual(user_dict["__class__"], "User")
        self.assertEqual(user_dict["email"], "test@example.com")
        self.assertEqual(user_dict["first_name"], "John")
        self.assertEqual(user_dict["id"], self.user.id)

if __name__ == '__main__':
    unittest.main()