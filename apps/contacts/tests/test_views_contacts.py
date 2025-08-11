from django.test import TestCase, RequestFactory
from django.urls import reverse, reverse_lazy

from apps.contacts.forms import FeedbackForm
from apps.contacts.models import ContactInfo, Branch, Feedback
from apps.contacts.views import ContactInfoView, BranchesListView, FeedbackCreateView
from apps.users.models import User


class ContactInfoViewTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.contact_info = ContactInfo.objects.create(
            address="Test Address",
            phone="1234567890",
            email="test@example.com",
            working_hours="9-18"
        )
        self.main_branch = Branch.objects.create(
            name="Main Branch",
            is_main=True,
            order=1
        )

    def test_template_used(self):
        response = self.client.get(reverse("contacts:contact-info"))
        self.assertTemplateUsed(response, "contacts/contact_info.html")

    def test_context_data(self):
        request = self.factory.get(reverse("contacts:contact-info"))
        response = ContactInfoView.as_view()(request)
        self.assertEqual(response.context_data["contact_info"], self.contact_info)
        self.assertEqual(response.context_data["branches"], self.main_branch)

    def test_no_contact_info(self):
        ContactInfo.objects.all().delete()
        response = self.client.get(reverse("contacts:contact-info"))
        self.assertIsNone(response.context["contact_info"])


class BranchesListViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.branch1 = Branch.objects.create(name="Branch 1", order=2)
        cls.branch2 = Branch.objects.create(name="Branch 2", order=1)
        cls.branch3 = Branch.objects.create(name="Branch 3", order=3)

    def test_view_uses_correct_template(self):
        view = BranchesListView()
        self.assertEqual(view.template_name, "contacts/branches_list.html")

    def test_view_ordering(self):
        view = BranchesListView()
        queryset = view.get_queryset()
        self.assertEqual(queryset[0].name, "Branch 2")
        self.assertEqual(queryset[1].name, "Branch 1")
        self.assertEqual(queryset[2].name, "Branch 3")

    def test_view_context_object_name(self):
        view = BranchesListView()
        self.assertEqual(view.context_object_name, "branches")


class FeedbackCreateViewTest(TestCase):
    def test_view_uses_correct_template(self):
        view = FeedbackCreateView()
        self.assertEqual(view.template_name, "contacts/feedback_form.html")

    def test_view_uses_correct_form_class(self):
        view = FeedbackCreateView()
        self.assertEqual(view.form_class, FeedbackForm)


class FeedbackThanksViewTest(TestCase):
    def test_template_used(self):
        response = self.client.get(reverse("contacts:feedback-thanks"))
        self.assertTemplateUsed(response, "contacts/feedback_thanks.html")


class FeedbackListViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        user = User.objects.create_user(username="testuser", password="12345")
        Feedback.objects.create(name="Feedback 1", email="test1@example.com", subject="Subject 1", message="Message 1")
        Feedback.objects.create(name="Feedback 2", email="test2@example.com", subject="Subject 2", message="Message 2")

    def test_login_required(self):
        response = self.client.get(reverse("contacts:feedback-list"))
        self.assertEqual(response.status_code, 302)

    def test_authenticated_access(self):
        self.client.login(username="testuser", password="12345")
        response = self.client.get(reverse("contacts:feedback-list"))
        self.assertEqual(response.status_code, 200)

    def test_ordering(self):
        self.client.login(username="testuser", password="12345")
        response = self.client.get(reverse("contacts:feedback-list"))
        feedbacks = response.context["feedbacks"]
        self.assertTrue(feedbacks[0].created_at > feedbacks[1].created_at)

    def test_pagination(self):
        self.client.login(username="testuser", password="12345")
        for i in range(25):
            Feedback.objects.create(
                name=f"Feedback {i+3}",
                email=f"test{i+3}@example.com",
                subject=f"Subject {i+3}",
                message=f"Message {i+3}"
            )
        response = self.client.get(reverse("contacts:feedback-list"))
        self.assertTrue(response.context["is_paginated"])
        self.assertEqual(len(response.context["feedbacks"]), 20)
