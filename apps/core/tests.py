from django.test import Client, TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from apps.core.models import TeamMember
from apps.users.models import User


class HomeViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username="testuser")

    def test_home_view_unauthenticated(self):
        response = self.client.get(reverse("home"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Welcome")

    def test_home_view_authenticated(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse("home"))
        self.assertContains(response, "Dashboard")


class TeamMemberAPITest(APITestCase):
    def setUp(self):
        self.member = TeamMember.objects.create(
            name="Dr. Smith", position="Cardiologist", bio="Expert in heart diseases"
        )

    def test_team_member_list(self):
        url = reverse("team-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["name"], "Dr. Smith")


class TemplateTests(TestCase):
    def test_base_template_extends(self):
        response = self.client.get(reverse("home"))
        self.assertTemplateUsed(response, "base.html")
        self.assertTemplateUsed(response, "core/home.html")
