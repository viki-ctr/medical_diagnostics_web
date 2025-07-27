from django.test import TestCase
from django.contrib.auth import get_user_model
from django.utils import timezone
from django.core.files.uploadedfile import SimpleUploadedFile
from rest_framework.test import APIClient
from rest_framework import status
from apps.users.models import DoctorProfile
from apps.services.models import Service, ServiceCategory
from .models import Appointment, DoctorSchedule

User = get_user_model()


class AppointmentModelTest(TestCase):
    def setUp(self):
        self.category = ServiceCategory.objects.create(name="General")
        self.service = Service.objects.create(
            name="Консультация",
            price=2000,
            duration=timezone.timedelta(minutes=30),
            category=self.category)
        self.patient = User.objects.create_user(
            username='patient1',
            password='testpass',
            is_patient=True
        )
        self.doctor_user = User.objects.create_user(
            username='doctor1',
            password='testpass',
            is_doctor=True
        )
        self.doctor = DoctorProfile.objects.create(
            user=self.doctor_user,
            specialty='cardiology'
        )
        self.service = Service.objects.create(
            name='Консультация',
            price=2000,
            duration=timezone.timedelta(minutes=30)
        )
        self.appointment = Appointment.objects.create(
            patient=self.patient,
            doctor=self.doctor,
            service=self.service,
            appointment_date=timezone.now() + timezone.timedelta(days=1))

    def test_appointment_creation(self):
        self.assertEqual(self.appointment.status, 'pending')
        self.assertEqual(self.appointment.patient.username, 'patient1')
        self.assertEqual(self.appointment.doctor.specialty, 'cardiology')

    def test_results_url_property(self):
        # Без файла
        self.assertIsNone(self.appointment.results_url)

        # С файлом
        test_file = SimpleUploadedFile("test.txt", b"file_content")
        self.appointment.results = test_file
        self.appointment.save()
        self.assertIn('test.txt', self.appointment.results_url)


class DoctorScheduleModelTest(TestCase):
    def setUp(self):
        self.category = ServiceCategory.objects.create(name="General")
        self.service = Service.objects.create(
            name="Консультация",
            price=2000,
            duration=timezone.timedelta(minutes=30),
            category=self.category)
        self.doctor_user = User.objects.create_user(
            username='doctor2',
            password='testpass',
            is_doctor=True
        )
        self.doctor = DoctorProfile.objects.create(
            user=self.doctor_user,
            specialty='neurology'
        )
        self.schedule = DoctorSchedule.objects.create(
            doctor=self.doctor,
            working_days=[0, 1, 2, 3, 4],
            working_hours={'start': '09:00', 'end': '18:00'},
            breaks=[{'start': '13:00', 'end': '14:00'}]
        )

    def test_schedule_creation(self):
        self.assertEqual(self.schedule.working_days, [0, 1, 2, 3, 4])
        self.assertEqual(self.schedule.working_hours['start'], '09:00')
        self.assertEqual(len(self.schedule.breaks), 1)


class AppointmentSerializerTest(TestCase):
    def setUp(self):
        self.category = ServiceCategory.objects.create(name="General")
        self.service = Service.objects.create(
            name="Консультация",
            price=2000,
            duration=timezone.timedelta(minutes=30),
            category=self.category)
        self.client = APIClient()
        self.patient = User.objects.create_user(
            username='patient2',
            password='testpass',
            is_patient=True
        )
        self.doctor_user = User.objects.create_user(
            username='doctor3',
            password='testpass',
            is_doctor=True
        )
        self.doctor = DoctorProfile.objects.create(
            user=self.doctor_user,
            specialty='pediatrics'
        )
        self.service = Service.objects.create(
            name='Осмотр',
            price=1500,
            duration=timezone.timedelta(minutes=45))
        self.appointment_data = {
            'doctor_id': self.doctor.id,
            'service_id': self.service.id,
            'appointment_date': timezone.now() + timezone.timedelta(days=2),
            'notes': 'Тестовая запись'
        }

    def test_appointment_serializer(self):
        from .serializers import AppointmentSerializer

        # Авторизуем пациента
        self.client.force_authenticate(user=self.patient)

        serializer = AppointmentSerializer(data=self.appointment_data)
        self.assertTrue(serializer.is_valid())

        # Проверка валидации даты в прошлом
        invalid_data = self.appointment_data.copy()
        invalid_data['appointment_date'] = timezone.now() - timezone.timedelta(days=1)
        serializer = AppointmentSerializer(data=invalid_data)
        self.assertFalse(serializer.is_valid())


class AppointmentViewSetTest(TestCase):
    def setUp(self):
        self.category = ServiceCategory.objects.create(name="General")
        self.service = Service.objects.create(
            name="Консультация",
            price=2000,
            duration=timezone.timedelta(minutes=30),
            category=self.category)
        self.client = APIClient()
        self.patient = User.objects.create_user(
            username='patient3',
            password='testpass',
            is_patient=True
        )
        self.doctor_user = User.objects.create_user(
            username='doctor4',
            password='testpass',
            is_doctor=True
        )
        self.doctor = DoctorProfile.objects.create(
            user=self.doctor_user,
            specialty='dentistry'
        )
        self.service = Service.objects.create(
            name='Чистка',
            price=3000,
            duration=timezone.timedelta(minutes=60))
        self.appointment = Appointment.objects.create(
            patient=self.patient,
            doctor=self.doctor,
            service=self.service,
            appointment_date=timezone.now() + timezone.timedelta(days=3))

    def test_get_appointments_as_patient(self):
        self.client.force_authenticate(user=self.patient)
        response = self.client.get('/api/appointments/appointments/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_get_appointments_as_doctor(self):
        self.client.force_authenticate(user=self.doctor_user)
        response = self.client.get('/api/appointments/appointments/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_create_appointment(self):
        self.client.force_authenticate(user=self.patient)
        data = {
            'doctor_id': self.doctor.id,
            'service_id': self.service.id,
            'appointment_date': timezone.now() + timezone.timedelta(days=4)
        }
        response = self.client.post('/api/appointments/appointments/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


class DoctorScheduleAPIViewTest(TestCase):
    def setUp(self):
        self.category = ServiceCategory.objects.create(name="General")
        self.service = Service.objects.create(
            name="Консультация",
            price=2000,
            duration=timezone.timedelta(minutes=30),
            category=self.category)
        self.client = APIClient()
        self.doctor_user = User.objects.create_user(
            username='doctor5',
            password='testpass',
            is_doctor=True
        )
        self.doctor = DoctorProfile.objects.create(
            user=self.doctor_user,
            specialty='surgery'
        )
        self.schedule_data = {
            'working_days': [1, 2, 3, 4, 5],
            'working_hours': {'start': '08:00', 'end': '17:00'},
            'breaks': [{'start': '12:00', 'end': '13:00'}]
        }

    def test_get_doctor_schedule(self):
        self.client.force_authenticate(user=self.doctor_user)
        response = self.client.get(f'/api/appointments/doctors/{self.doctor.id}/schedule/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_doctor_schedule(self):
        self.client.force_authenticate(user=self.doctor_user)
        response = self.client.put(
            f'/api/appointments/doctors/{self.doctor.id}/schedule/',
            data=self.schedule_data,
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['working_hours']['start'], '08:00')


class AvailableTimeSlotsAPIViewTest(TestCase):
    def setUp(self):
        self.category = ServiceCategory.objects.create(name="General")
        self.service = Service.objects.create(
            name="Консультация",
            price=2000,
            duration=timezone.timedelta(minutes=30),
            category=self.category)
        self.client = APIClient()
        self.doctor_user = User.objects.create_user(
            username='doctor6',
            password='testpass',
            is_doctor=True
        )
        self.doctor = DoctorProfile.objects.create(
            user=self.doctor_user,
            specialty='orthopedics'
        )
        self.service = Service.objects.create(
            name='Рентген',
            price=2500,
            duration=timezone.timedelta(minutes=15))
        self.schedule = DoctorSchedule.objects.create(
            doctor=self.doctor,
            working_days=[0, 1, 2, 3, 4],
            working_hours={'start': '09:00', 'end': '18:00'}
        )
        self.tomorrow = timezone.now().date() + timezone.timedelta(days=1)

    def test_get_available_slots(self):
        self.client.force_authenticate(user=self.doctor_user)
        response = self.client.get(
            '/api/appointments/available-slots/',
            {
                'doctor': self.doctor.id,
                'service': self.service.id,
                'date': self.tomorrow.strftime('%Y-%m-%d')
            }
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreater(len(response.data['slots']), 0)
