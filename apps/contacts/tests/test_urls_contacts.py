from django.test import TestCase
from django.urls import reverse, resolve

from apps.contacts.views import ContactInfoView, BranchesListView, FeedbackCreateView, FeedbackThanksView, \
    FeedbackListView, FeedbackUpdateView


class TestUrls(TestCase):
    def test_contact_info_url(self):
        url = reverse("contacts:contact-info")
        self.assertEqual(resolve(url).func.view_class, ContactInfoView)

    def test_branches_list_url(self):
        url = reverse("contacts:branches-list")
        self.assertEqual(resolve(url).func.view_class, BranchesListView)

    def test_feedback_form_url(self):
        url = reverse("contacts:feedback-form")
        self.assertEqual(resolve(url).func.view_class, FeedbackCreateView)

    def test_feedback_thanks_url(self):
        url = reverse("contacts:feedback-thanks")
        self.assertEqual(resolve(url).func.view_class, FeedbackThanksView)

    def test_feedback_list_url(self):
        url = reverse("contacts:feedback-list")
        self.assertEqual(resolve(url).func.view_class, FeedbackListView)

    def test_feedback_update_url(self):
        url = reverse("contacts:feedback-update", kwargs={"pk": 1})
        self.assertEqual(resolve(url).func.view_class, FeedbackUpdateView)
