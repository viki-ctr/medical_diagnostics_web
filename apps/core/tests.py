from django.test import TestCase
from django.urls import reverse
from apps.services.models import Service


class CoreViewsTest(TestCase):
    def setUp(self):
        self.service = Service.objects.create(
            name='Test Service',
            description='Test Description',
            price=1000.00,
            duration='00:30:00'
        )

    def test_home_view(self):
        response = self.client.get(reverse('core:home'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'core/index.html')
        self.assertContains(response, 'Добро пожаловать')
        self.assertIn('popular_services', response.context)
