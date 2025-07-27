from django.test import TestCase
from django.contrib.auth import get_user_model
from apps.users.models import PatientProfile, DoctorProfile


User = get_user_model()


class UserModelTest(TestCase):
    def test_create_user(self):
        user = User.objects.create_user(
            username='patient1',
            email='patient@test.com',
            password='testpass123',
            is_patient=True
        )
        self.assertEqual(user.username, 'patient1')
        self.assertTrue(user.is_patient)
        self.assertFalse(user.is_doctor)

    def test_create_superuser(self):
        admin_user = User.objects.create_superuser(
            username='admin',
            email='admin@test.com',
            password='testpass123'
        )
        self.assertTrue(admin_user.is_superuser)
        self.assertTrue(admin_user.is_staff)


class PatientProfileModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='patient1',
            email='patient@test.com',
            password='testpass123',
            is_patient=True
        )
        self.profile = PatientProfile.objects.create(
            user=self.user,
            birth_date='1990-01-01',
            address='Test address 123'
        )

    def test_profile_creation(self):
        self.assertEqual(self.profile.user.username, 'patient1')
        self.assertEqual(str(self.profile), 'patient1 profile')


class DoctorProfileModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='doctor1',
            email='doctor@test.com',
            password='testpass123',
            is_doctor=True
        )
        self.profile = DoctorProfile.objects.create(
            user=self.user,
            specialty='Cardiology',
            bio='Test bio'
        )

    def test_profile_creation(self):
        self.assertEqual(self.profile.specialty, 'Cardiology')
        self.assertEqual(str(self.profile), 'doctor1 profile')
