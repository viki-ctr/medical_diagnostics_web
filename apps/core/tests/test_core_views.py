from django.test import TestCase, RequestFactory
from django.urls import reverse
from django.contrib.auth import get_user_model

from apps.core.models import SiteSetting, HomePageContent, AboutPage, Department, TeamMember, Testimonial, FAQCategory, \
    FAQ

User = get_user_model()


class CoreViewsTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.site_settings = SiteSetting.objects.create(
            site_name="Test Clinic",
            phone="1234567890",
            email="test@example.com",
            address="Test Address"
        )

        cls.home_content = HomePageContent.objects.create(
            main_title="Welcome",
            main_description="Test description",
            is_active=True
        )

        cls.about_page = AboutPage.objects.create(
            title="About Us",
            content="About content",
            is_active=True
        )

        cls.department = Department.objects.create(
            name="Cardiology",
            description="Heart department"
        )

        cls.team_member = TeamMember.objects.create(
            name="Dr. Smith",
            position="Cardiologist",
            department=cls.department,
            is_visible=True
        )

        cls.testimonial = Testimonial.objects.create(
            author="Patient",
            content="Great service",
            is_featured=True
        )

        cls.faq_category = FAQCategory.objects.create(
            name="General",
            slug="general"
        )

        cls.faq = FAQ.objects.create(
            question="How to book?",
            answer="Call us",
            category=cls.faq_category,
            is_active=True
        )


class HomeViewTest(CoreViewsTest):
    def test_home_view_status_code(self):
        response = self.client.get(reverse("core:home"))
        self.assertEqual(response.status_code, 200)

    def test_home_view_template(self):
        response = self.client.get(reverse("core:home"))
        self.assertTemplateUsed(response, "core/index.html")

    def test_home_view_context(self):
        response = self.client.get(reverse("core:home"))
        self.assertIn("home_content", response.context)
        self.assertIn("testimonials", response.context)
        self.assertIn("site_settings", response.context)
        self.assertEqual(response.context["home_content"], self.home_content)
        self.assertIn(self.testimonial, response.context["testimonials"])
        self.assertEqual(response.context["site_settings"], self.site_settings)


class AboutViewTest(CoreViewsTest):
    def test_about_view_status_code(self):
        response = self.client.get(reverse("core:about"))
        self.assertEqual(response.status_code, 200)

    def test_about_view_template(self):
        response = self.client.get(reverse("core:about"))
        self.assertTemplateUsed(response, "core/about.html")

    def test_about_view_context(self):
        response = self.client.get(reverse("core:about"))
        self.assertIn("about_page", response.context)
        self.assertIn("team_members", response.context)
        self.assertIn("departments", response.context)
        self.assertEqual(response.context["about_page"], self.about_page)
        self.assertIn(self.team_member, response.context["team_members"])
        self.assertIn(self.department, response.context["departments"])


class FAQListViewTest(CoreViewsTest):
    def test_faq_list_view_status_code(self):
        response = self.client.get(reverse("core:faq_list"))
        self.assertEqual(response.status_code, 200)

    def test_faq_list_view_template(self):
        response = self.client.get(reverse("core:faq_list"))
        self.assertTemplateUsed(response, "core/faq_list.html")

    def test_faq_list_view_context(self):
        response = self.client.get(reverse("core:faq_list"))
        self.assertIn("faqs", response.context)
        self.assertIn("categories", response.context)
        self.assertIn(self.faq, response.context["faqs"])
        self.assertIn(self.faq_category, response.context["categories"])

    def test_faq_list_view_queryset(self):
        FAQ.objects.create(
            question="Inactive",
            answer="Test",
            is_active=False
        )
        response = self.client.get(reverse("core:faq_list"))
        self.assertEqual(len(response.context["faqs"]), 1)
        self.assertEqual(response.context["faqs"][0], self.faq)


class FAQCategoryViewTest(CoreViewsTest):
    def test_faq_category_view_status_code(self):
        url = reverse("core:faq_category", kwargs={"slug": self.faq_category.slug})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_faq_category_view_template(self):
        url = reverse("core:faq_category", kwargs={"slug": self.faq_category.slug})
        response = self.client.get(url)
        self.assertTemplateUsed(response, "core/faq_category.html")

    def test_faq_category_view_context(self):
        url = reverse("core:faq_category", kwargs={"slug": self.faq_category.slug})
        response = self.client.get(url)
        self.assertIn("category", response.context)
        self.assertIn("faqs", response.context)
        self.assertEqual(response.context["category"], self.faq_category)
        self.assertIn(self.faq, response.context["faqs"])

    def test_faq_category_view_404(self):
        url = reverse("core:faq_category", kwargs={"slug": "nonexistent"})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)


class TeamListViewTest(CoreViewsTest):
    def test_team_list_view_status_code(self):
        response = self.client.get(reverse("core:team_list"))
        self.assertEqual(response.status_code, 200)

    def test_team_list_view_template(self):
        response = self.client.get(reverse("core:team_list"))
        self.assertTemplateUsed(response, "core/team_list.html")

    def test_team_list_view_context(self):
        response = self.client.get(reverse("core:team_list"))
        self.assertIn("team_members", response.context)
        self.assertIn("departments", response.context)
        self.assertIn(self.team_member, response.context["team_members"])
        self.assertIn(self.department, response.context["departments"])

    def test_team_list_view_queryset(self):
        TeamMember.objects.create(
            name="Invisible",
            position="Test",
            is_visible=False
        )
        response = self.client.get(reverse("core:team_list"))
        self.assertEqual(len(response.context["team_members"]), 1)
        self.assertEqual(response.context["team_members"][0], self.team_member)


class TestimonialListViewTest(CoreViewsTest):
    def test_testimonial_list_view_status_code(self):
        response = self.client.get(reverse("core:testimonial_list"))
        self.assertEqual(response.status_code, 200)

    def test_testimonial_list_view_template(self):
        response = self.client.get(reverse("core:testimonial_list"))
        self.assertTemplateUsed(response, "core/testimonial_list.html")

    def test_testimonial_list_view_context(self):
        response = self.client.get(reverse("core:testimonial_list"))
        self.assertIn("testimonials", response.context)
        self.assertIn(self.testimonial, response.context["testimonials"])

    def test_testimonial_list_view_pagination(self):
        for i in range(15):
            Testimonial.objects.create(
                author=f"Patient {i}",
                content=f"Testimonial {i}"
            )
        response = self.client.get(reverse("core:testimonial_list"))
        self.assertTrue(response.context["is_paginated"])
        self.assertEqual(len(response.context["testimonials"]), 10)


class DepartmentDetailViewTest(CoreViewsTest):
    def test_department_detail_view_status_code(self):
        url = reverse("core:department_detail", kwargs={"pk": self.department.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_department_detail_view_template(self):
        url = reverse("core:department_detail", kwargs={"pk": self.department.pk})
        response = self.client.get(url)
        self.assertTemplateUsed(response, "core/department_detail.html")

    def test_department_detail_view_context(self):
        url = reverse("core:department_detail", kwargs={"pk": self.department.pk})
        response = self.client.get(url)
        self.assertIn("department", response.context)
        self.assertIn("team_members", response.context)
        self.assertEqual(response.context["department"], self.department)
        self.assertIn(self.team_member, response.context["team_members"])

    def test_department_detail_view_404(self):
        url = reverse("core:department_detail", kwargs={"pk": 999})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)
