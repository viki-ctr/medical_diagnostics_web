from django.test import TestCase
from django.urls import reverse
from apps.services.models import Service


class TemplateTests(TestCase):
    def setUp(self):
        self.service = Service.objects.create(
            name='Template Test Service',
            description='Template Test',
            price=2500.00,
            duration='01:30:00'
        )

    def test_base_template_used(self):
        response = self.client.get(reverse('services:list'))
        self.assertTemplateUsed(response, 'base.html')
        self.assertTemplateUsed(response, 'services/list.html')

    def test_service_detail_template_content(self):
        response = self.client.get(reverse('services:detail', args=[self.service.id]))
        self.assertContains(response, 'Template Test Service')
        self.assertContains(response, '2500.00')
        self.assertContains(response, 'Book Appointment')
        