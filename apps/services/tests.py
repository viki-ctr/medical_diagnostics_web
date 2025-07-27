from django.test import TestCase
from django.urls import reverse
from apps.services.models import ServiceCategory, Service


class ServiceCategoryModelTest(TestCase):
    def setUp(self):
        self.category = ServiceCategory.objects.create(
            name='Laboratory',
            description='Laboratory tests'
        )

    def test_category_creation(self):
        self.assertEqual(self.category.name, 'Laboratory')
        self.assertEqual(str(self.category), 'Laboratory')


class ServiceModelTest(TestCase):
    def setUp(self):
        self.category = ServiceCategory.objects.create(
            name='Laboratory',
            description='Laboratory tests'
        )
        self.service = Service.objects.create(
            category=self.category,
            name='Blood test',
            description='Complete blood count',
            price=1000.00,
            duration='00:30:00'
        )

    def test_service_creation(self):
        self.assertEqual(self.service.name, 'Blood test')
        self.assertEqual(self.service.price, 1000.00)
        self.assertEqual(str(self.service), 'Blood test')


class ServiceViewsTest(TestCase):
    def setUp(self):
        self.category = ServiceCategory.objects.create(
            name='Laboratory',
            description='Lab tests'
        )
        self.service = Service.objects.create(
            category=self.category,
            name='Blood test',
            description='Complete blood count',
            price=1000.00,
            duration='00:30:00'
        )

    def test_service_list_view(self):
        response = self.client.get(reverse('services:list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'services/list.html')
        self.assertIn('services', response.context)
        self.assertContains(response, 'Blood test')

    def test_service_detail_view(self):
        response = self.client.get(reverse('services:detail', args=[self.service.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'services/detail.html')
        self.assertEqual(response.context['service'], self.service)
        self.assertContains(response, 'Complete blood count')
