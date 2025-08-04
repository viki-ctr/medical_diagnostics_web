from django.test import TestCase
from django.urls import reverse, resolve

from apps.core.views import HomeView, AboutView, FAQListView, FAQCategoryView, TeamListView, DepartmentDetailView, \
    TestimonialListView


class TestCoreUrls(TestCase):
    def test_home_url_resolves(self):
        url = reverse("core:home")
        self.assertEqual(resolve(url).func.view_class, HomeView)
        self.assertEqual(url, "/")

    def test_about_url_resolves(self):
        url = reverse("core:about")
        self.assertEqual(resolve(url).func.view_class, AboutView)
        self.assertEqual(url, "/about/")

    def test_faq_list_url_resolves(self):
        url = reverse("core:faq_list")
        self.assertEqual(resolve(url).func.view_class, FAQListView)
        self.assertEqual(url, "/faq/")

    def test_faq_category_url_resolves(self):
        url = reverse("core:faq_category", kwargs={"slug": "general"})
        self.assertEqual(resolve(url).func.view_class, FAQCategoryView)
        self.assertEqual(url, "/faq/category/general/")

    def test_team_list_url_resolves(self):
        url = reverse("core:team_list")
        self.assertEqual(resolve(url).func.view_class, TeamListView)
        self.assertEqual(url, "/team/")

    def test_department_detail_url_resolves(self):
        url = reverse("core:department_detail", kwargs={"pk": 1})
        self.assertEqual(resolve(url).func.view_class, DepartmentDetailView)
        self.assertEqual(url, "/team/department/1/")

    def test_testimonial_list_url_resolves(self):
        url = reverse("core:testimonial_list")
        self.assertEqual(resolve(url).func.view_class, TestimonialListView)
        self.assertEqual(url, "/testimonials/")
