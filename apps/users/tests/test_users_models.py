from django.test import TestCase
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model

from ..models import PatientProfile, DoctorProfile

User = get_user_model()


class UserModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )

    def test_user_creation(self):
        self.assertEqual(self.user.username, 'testuser')
        self.assertEqual(self.user.email, 'test@example.com')
        self.assertTrue(self.user.check_password('testpass123'))
        self.assertFalse(self.user.is_patient)
        self.assertFalse(self.user.is_doctor)

    def test_user_str_representation(self):
        self.assertEqual(str(self.user), 'testuser')

    def test_user_types(self):
        patient_user = User.objects.create_user(
            username='patient',
            password='testpass123',
            is_patient=True
        )
        self.assertTrue(patient_user.is_patient)
        self.assertFalse(patient_user.is_doctor)

        doctor_user = User.objects.create_user(
            username='doctor',
            password='testpass123',
            is_doctor=True
        )
        self.assertTrue(doctor_user.is_doctor)
        self.assertFalse(doctor_user.is_patient)


class PatientProfileModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='patientuser',
            password='testpass123',
            is_patient=True
        )
        self.patient_profile = PatientProfile.objects.create(
            user=self.user,
            birth_date='2000-01-01',
            gender='M',
            address='Test Address',
            phone='+79991234567',
            medical_history='Some medical history'
        )

    def test_patient_profile_creation(self):
        self.assertEqual(self.patient_profile.user.username, 'patientuser')
        self.assertEqual(str(self.patient_profile.birth_date), '2000-01-01')
        self.assertEqual(self.patient_profile.gender, 'M')
        self.assertEqual(self.patient_profile.address, 'Test Address')
        self.assertEqual(self.patient_profile.phone, '+79991234567')
        self.assertEqual(self.patient_profile.medical_history, 'Some medical history')

    def test_patient_profile_str_representation(self):
        self.assertEqual(str(self.patient_profile), 'Профиль пациента: patientuser')

    def test_patient_profile_blank_fields(self):
        PatientProfile.objects.filter(user=self.user).delete()
        profile = PatientProfile.objects.create(user=self.user)
        self.assertIsNone(profile.birth_date)
        self.assertEqual(profile.gender, '')
        self.assertEqual(profile.address, '')
        self.assertEqual(profile.phone, '')
        self.assertEqual(profile.medical_history, '')

    def test_patient_profile_gender_choices(self):
        # Создаем нового пользователя для теста
        test_user = User.objects.create_user(username='testuser2', password='testpass123')
        valid_choices = ['M', 'F', 'O']
        for choice in valid_choices:
            PatientProfile.objects.filter(user=test_user).delete()
            profile = PatientProfile(user=test_user, gender=choice)
            profile.full_clean()

        with self.assertRaises(ValidationError):
            PatientProfile.objects.filter(user=test_user).delete()
            profile = PatientProfile(user=test_user, gender='X')
            profile.full_clean()


class DoctorProfileModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='doctoruser',
            password='testpass123',
            is_doctor=True
        )
        self.doctor_profile = DoctorProfile.objects.create(
            user=self.user,
            specialty='Кардиология',
            department='Кардиологическое отделение',
            bio='Опытный кардиолог'
        )

    def test_doctor_profile_creation(self):
        self.assertEqual(self.doctor_profile.user.username, 'doctoruser')
        self.assertEqual(self.doctor_profile.specialty, 'Кардиология')
        self.assertEqual(self.doctor_profile.department, 'Кардиологическое отделение')
        self.assertEqual(self.doctor_profile.bio, 'Опытный кардиолог')

    def test_doctor_profile_str_representation(self):
        self.assertEqual(str(self.doctor_profile), 'Профиль врача: doctoruser (Кардиология)')

    def test_doctor_profile_default_values(self):
        new_user = User.objects.create_user(username='newdoctor', password='testpass123')
        profile = DoctorProfile.objects.create(user=new_user)
        self.assertEqual(profile.department, 'Общее отделение')
        self.assertIsNone(profile.bio)

    def test_doctor_profile_blank_fields(self):
        new_user = User.objects.create_user(username='doctor2', password='testpass123')
        profile = DoctorProfile.objects.create(
            user=new_user,
            specialty='Терапевт',
            bio=''
        )
        self.assertEqual(profile.bio, '')

    def test_doctor_profile_max_lengths(self):
        new_user = User.objects.create_user(username='doctor3', password='testpass123')
        profile = DoctorProfile(
            user=new_user,
            specialty='A' * 100,
            department='B' * 100
        )
        profile.full_clean()

        with self.assertRaises(ValidationError):
            profile.specialty = 'A' * 101
            profile.full_clean()

        with self.assertRaises(ValidationError):
            profile.department = 'B' * 101
            profile.full_clean()


class ProfileRelationshipsTest(TestCase):
    def test_user_patient_profile_relationship(self):
        user = User.objects.create_user(username='patient1', is_patient=True)
        profile = PatientProfile.objects.create(user=user)

        self.assertEqual(user.patient_profile, profile)
        self.assertEqual(profile.user, user)

    def test_user_doctor_profile_relationship(self):
        user = User.objects.create_user(username='doctor1', is_doctor=True)
        profile = DoctorProfile.objects.create(user=user)

        self.assertEqual(user.doctor_profile, profile)
        self.assertEqual(profile.user, user)

    def test_user_can_have_both_profiles(self):
        user = User.objects.create_user(username='testuser')

        patient_profile = PatientProfile.objects.create(user=user)

        doctor_profile = DoctorProfile.objects.create(user=user)

        self.assertEqual(user.patient_profile, patient_profile)
        self.assertEqual(user.doctor_profile, doctor_profile)
        self.assertTrue(hasattr(user, 'patient_profile'))
        self.assertTrue(hasattr(user, 'doctor_profile'))
