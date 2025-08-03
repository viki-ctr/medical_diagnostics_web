from django.test import SimpleTestCase
from django.urls import reverse, resolve

from apps.services import views


class TestServicesUrls(SimpleTestCase):
    def test_service_home_url_resolves(self):
        url = reverse("services:home")
        self.assertEqual(resolve(url).func.view_class, views.ServiceHomeView)
        self.assertEqual(url, "/services/")  # Изменено с "/" на "/services/"

    def test_all_services_url_resolves(self):
        url = reverse("services:all_services")
        self.assertEqual(resolve(url).func.view_class, views.AllServicesView)
        self.assertEqual(url, "/services/services/")  # Ожидаемый путь с учетом префикса

    def test_service_category_list_url_resolves(self):
        url = reverse("services:list")
        self.assertEqual(resolve(url).func.view_class, views.ServiceCategoryListView)
        self.assertEqual(url, "/services/services/category/")  # Ожидаемый путь

    def test_service_category_list_with_slug_url_resolves(self):
        url = reverse("services:list_by_category", kwargs={"slug": "web-development"})
        self.assertEqual(resolve(url).func.view_class, views.ServiceCategoryListView)
        self.assertEqual(url, "/services/services/category/web-development/")  # Ожидаемый путь

    def test_service_detail_url_resolves(self):
        url = reverse("services:detail", kwargs={"slug": "seo-optimization"})
        self.assertEqual(resolve(url).func.view_class, views.ServiceDetailView)
        self.assertEqual(url, "/services/services/seo-optimization/")
