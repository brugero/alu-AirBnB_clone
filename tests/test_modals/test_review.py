#!/usr/bin/python3
"""Unit tests for Review class"""
import unittest
from datetime import datetime
from models.review import Review
from models import storage
import os

class TestReview(unittest.TestCase):
    """Test cases for Review class"""

    def setUp(self):
        """Set up test environment"""
        self.review = Review()
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
        self.assertEqual(self.review.place_id, "")
        self.assertEqual(self.review.user_id, "")
        self.assertEqual(self.review.text, "")
        self.assertIsInstance(self.review.id, str)
        self.assertIsInstance(self.review.created_at, datetime)
        self.assertIsInstance(self.review.updated_at, datetime)

    def test_init_with_kwargs(self):
        """Test initialization with kwargs"""
        dict_data = {
            "id": "123e4567-e89b-12d3-a456-426614174000",
            "created_at": datetime.now().isoformat(),
            "updated_at": datetime.now().isoformat(),
            "place_id": "place-123",
            "user_id": "user-123",
            "text": "Great stay!",
            "__class__": "Review"
        }
        review = Review(**dict_data)
        self.assertEqual(review.place_id, "place-123")
        self.assertEqual(review.user_id, "user-123")
        self.assertEqual(review.text, "Great stay!")
        self.assertIsInstance(review.created_at, datetime)

    def test_str(self):
        """Test string representation"""
        self.review.text = "Great stay!"
        str_rep = str(self.review)
        expected = f"[Review] ({self.review.id}) {self.review.__dict__}"
        self.assertEqual(str_rep, expected)

    def test_save(self):
        """Test save method"""
        old_updated_at = self.review.updated_at
        self.review.save()
        self.assertNotEqual(old_updated_at, self.review.updated_at)
        self.assertTrue(os.path.exists(self.file_path))

    def test_to_dict(self):
        """Test to_dict method"""
        self.review.text = "Great stay!"
        review_dict = self.review.to_dict()
        self.assertEqual(review_dict["__class__"], "Review")
        self.assertEqual(review_dict["text"], "Great stay!")
        self.assertEqual(review_dict["id"], self.review.id)

if __name__ == '__main__':
    unittest.main()