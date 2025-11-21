from django.test import TestCase
from .forms import CommentForm


class TestCommentForm(TestCase):

    def test_form_is_valid(self):
        """Test when all required fields have values"""

        comment_form = CommentForm({"body": "Body content."})
        error_message = "Form is not valid when it should be valid"
        self.assertTrue(comment_form.is_valid(), error_message)

    def test_form_is_invalid(self):
        """Test when a required field has no value"""

        comment_form = CommentForm({"body": ""})
        error_message = "Form is valid when it should be invalid."
        self.assertFalse(comment_form.is_valid(), error_message)
