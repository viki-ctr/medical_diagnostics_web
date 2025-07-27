from django.test import TestCase
from django.contrib.auth import get_user_model
from apps.users.models import DoctorProfile


User = get_user_model()


class DoctorProfileModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(
            username='doctor1',
            email='doctor@test.com',
            password='testpass123',
            is_doctor=True
        )
        cls.profile = DoctorProfile.objects.create(
            user=cls.user,
            specialty='Cardiology',
            bio='Test bio'
        )

    def test_profile_creation(self):
        self.assertEqual(self.profile.user.username, 'doctor1')
        self.assertEqual(self.profile.specialty, 'Cardiology')

    def test_str_representation(self):
        self.assertEqual(str(self.profile), f"{self.user.username} profile")


class UserSignalsTest(TestCase):
    def test_doctor_profile_creation(self):
        user = User.objects.create_user(
            username="dr_test",
            email="dr@test.com",
            password="testpass",
            is_doctor=True
        )
        self.assertTrue(hasattr(user, 'doctorprofile'))
        self.assertEqual(user.doctorprofile.specialty, 'General')
