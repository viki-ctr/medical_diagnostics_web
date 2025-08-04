from django.test import TestCase
from django.urls import reverse
from model_bakery import baker
from apps.services.models import Service, ServiceCategory


class ServiceHomeViewTest(TestCase):
    def setUp(self):
        self.category = baker.make(ServiceCategory)
        self.services = baker.make(Service, is_available=True, category=self.category, _quantity=10)

    def test_home_view(self):
        url = reverse("services:home")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "services/home.html")


class ServiceCategoryListViewTest(TestCase):
    def setUp(self):
        self.category = baker.make(ServiceCategory)
        self.services = baker.make(
            Service,
            is_available=True,
            category=self.category,
            _quantity=15
        )

    def test_category_list_view(self):
        url = reverse("services:list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context["services"]), 10)

    def test_category_list_by_category_view(self):
        url = reverse("services:list_by_category", kwargs={"slug": self.category.slug})
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertIn('category', response.context)
        self.assertEqual(response.context['category'], self.category)
        self.assertEqual(len(response.context['services']), 10)
        self.assertTrue(response.context['services'].query.where.children[0].rhs, self.category.id)


class ServiceDetailViewTest(TestCase):
    def setUp(self):
        self.category = baker.make(ServiceCategory)
        self.service = baker.make(Service, is_available=True, category=self.category)
        self.related_services = baker.make(Service, is_available=True, category=self.category, _quantity=4)

    def test_service_detail_view(self):
        url = reverse("services:detail", kwargs={"slug": self.service.slug})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["service"], self.service)
        self.assertEqual(len(response.context["related_services"]), 4)


class AllServicesViewTest(TestCase):
    def setUp(self):
        self.services = baker.make(Service, is_available=True, _quantity=15)

    def test_all_services_view(self):
        url = reverse("services:all_services")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context["services"]), 12)
