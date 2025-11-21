from django.test import TestCase
from .forms import CollaborateForm


class TestCollaborateForm(TestCase):

    def test_form_is_valid(self):
        """Test when all fields are present"""

        test_form = CollaborateForm(
            {
                "name": "Test Name",
                "email": "text@example.com",
                "message": "Test message.",
            }
        )
        error_message = "CollaborateForm is invalid when it should be valid"
        self.assertTrue(test_form.is_valid(), error_message)

    def test_missing_name(self):
        """Test that the form is invalid when `name` is missing"""

        test_form = CollaborateForm(
            {
                "name": "",
                "email": "text@example.com",
                "message": "Test message.",
            }
        )
        error_message = "Form is incorrectly valid when `name` is missing"
        self.assertFalse(test_form.is_valid(), error_message)

    def test_missing_email(self):
        """Test that the form is invalid when `email` is missing"""

        test_form = CollaborateForm(
            {
                "name": "Test Name",
                "email": "",
                "message": "Test message.",
            }
        )
        error_message = "Form is incorrectly valid when `email` is missing"
        self.assertFalse(test_form.is_valid(), error_message)

    def test_missing_message(self):
        """Test that the form is invalid when `message` is missing"""

        test_form = CollaborateForm(
            {
                "name": "Test Name",
                "email": "test@example.com",
                "message": "",
            }
        )
        error_message = "Form is incorrectly valid when `message` is missing"
        self.assertFalse(test_form.is_valid(), error_message)
