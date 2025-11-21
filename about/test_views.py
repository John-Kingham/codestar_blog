from http import HTTPStatus
from django.test import TestCase
from django.urls import reverse
from .forms import CollaborateForm
from .models import About


class TestAboutView(TestCase):

    def setUp(self):
        self.about_view_path = "about-path"
        self.about = About(title="About title", content="About content")
        self.about.save()

    def test_render_about_page_with_collaborate_request_form(self):
        response = self.client.get(reverse(self.about_view_path))
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertIsInstance(response.context["about"], About)
        self.assertIsInstance(
            response.context["collaborate_form"], CollaborateForm
        )
        self.assertIn(bytes(self.about.title, "UTF-8"), response.content)

    def test_successful_collaborate_request_submission(self):
        collaborate_form_data = {
            "name": "Test name",
            "email": "test@example.com",
            "message": "Test message",
        }
        response = self.client.post(
            reverse(self.about_view_path), collaborate_form_data
        )
        self.assertEqual(response.status_code, HTTPStatus.OK)
        success_message = (
            "Collaboration request received! I endeavour to respond "
            "within 2 working days."
        )
        self.assertIn(bytes(success_message, "UTF-8"), response.content)
