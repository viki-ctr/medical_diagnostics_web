from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from apps.services.models import Service
from apps.appointments.models import Appointment

User = get_user_model()


class AppointmentFlowTest(TestCase):
    def setUp(self):
        # Создаем тестового пользователя
        self.user = User.objects.create_user(
            username='testpatient',
            email='patient@test.com',
            password='testpass123',
            is_patient=True
        )

        # Создаем тестовую услугу
        self.service = Service.objects.create(
            name='Integration Test Service',
            description='Integration Test',
            price=2000.00,
            duration='01:00:00'
        )

        # Авторизуем пользователя
        self.client.login(username='testpatient', password='testpass123')

    def test_appointment_flow(self):
        # Шаг 1: Просмотр списка услуг
        service_list_url = reverse('services:list')
        response = self.client.get(service_list_url)
        self.assertContains(response, 'Integration Test Service')

        # Шаг 2: Просмотр деталей услуги
        service_detail_url = reverse('services:detail', args=[self.service.id])
        response = self.client.get(service_detail_url)
        self.assertContains(response, 'Book Appointment')

        # Шаг 3: Создание записи
        appointment_create_url = reverse('appointments:create')
        response = self.client.post(appointment_create_url, {
            'service': self.service.id,
            'appointment_date': '2023-12-01 10:00',
            'notes': 'Integration test notes'
        }, follow=True)

        # Проверяем, что запись создана
        self.assertEqual(response.status_code, 200)
        self.assertTrue(Appointment.objects.exists())
        appointment = Appointment.objects.first()
        self.assertEqual(appointment.patient, self.user)
        self.assertEqual(appointment.service, self.service)

        # Шаг 4: Просмотр списка записей
        appointment_list_url = reverse('appointments:list')
        response = self.client.get(appointment_list_url)
        self.assertContains(response, 'Integration Test Service')
        