from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from apps.services.models import Service


class ServiceAPITest(APITestCase):
    def setUp(self):
        self.service = Service.objects.create(
            name='API Test Service',
            description='API Test Description',
            price=1500.00,
            duration='00:45:00'
        )

    def test_service_list_api(self):
        url = reverse('api:service-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['name'], 'API Test Service')

    def test_service_detail_api(self):
        url = reverse('api:service-detail', args=[self.service.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'API Test Service')
