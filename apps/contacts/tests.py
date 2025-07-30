from django.test import TestCase

from apps.contacts.forms import FeedbackForm


class FeedbackFormTest(TestCase):
    def test_valid_form(self):
        form_data = {
            "name": "John Doe",
            "email": "john@example.com",
            "phone": "+1234567890",
            "subject": "Test subject",
            "message": "Test message",
        }
        form = FeedbackForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_invalid_form_missing_name(self):
        form_data = {"email": "john@example.com", "subject": "Test subject", "message": "Test message"}
        form = FeedbackForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn("name", form.errors)
