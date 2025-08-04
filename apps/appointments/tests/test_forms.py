from datetime import timedelta
from django.utils import timezone

from django.contrib.auth import get_user_model
from django.db import transaction
from django.test import TestCase

from apps.appointments.forms import AppointmentForm, DoctorScheduleForm
from apps.services.models import Service, ServiceCategory
from apps.users.models import DoctorProfile, PatientProfile

User = get_user_model()


class AppointmentFormTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.category = ServiceCategory.objects.create(
            name="Основные услуги",
            slug="main-services",
            description="Описание категории",
            icon="fa-heart",
            is_main=True,
        )

        cls.service = Service.objects.create(
            category=cls.category,
            name="Консультация",
            slug="consultation",
            description="Описание услуги",
            price=1000.00,
            duration=timedelta(minutes=30),
            is_available=True,
            preparation="Подготовка не требуется",
        )

        cls.doctor_user = User.objects.create_user(
            username="doctor",
            password="testpass123",
            email="doctor@example.com",
            is_doctor=True,
            first_name="Иван",
            last_name="Петров"
        )
        cls.patient_user = User.objects.create_user(
            username="patient",
            password="testpass123",
            email="patient@example.com",
            is_patient=True,
            first_name="Мария",
            last_name="Сидорова"
        )

        cls.doctor = DoctorProfile.objects.create(
            user=cls.doctor_user,
            specialty="Терапевт",
            department="Терапевтическое отделение"
        )
        cls.patient = PatientProfile.objects.create(
            user=cls.patient_user,
            gender="M",
            phone="+79991234567"
        )

    def test_form_fields(self):
        """Тест наличия полей формы"""
        form = AppointmentForm()
        self.assertIn("doctor", form.fields)
        self.assertIn("service", form.fields)
        self.assertIn("appointment_date", form.fields)
        self.assertIn("notes", form.fields)

    def test_form_validation_valid_data(self):
        """Тест валидации с корректными данными"""
        form_data = {
            'doctor': self.doctor.id,
            'service': self.service.id,
            'appointment_date': '2024-01-01T10:00',
            'notes': 'Тестовая запись'
        }
        form = AppointmentForm(data=form_data)
        self.assertTrue(form.is_valid(), f"Form errors: {form.errors}")


    def test_form_for_doctor_user(self):
        """Тест формы для пользователя-врача"""
        form = AppointmentForm(user=self.doctor_user)
        self.assertEqual(form.fields["doctor"].initial, self.doctor)
        self.assertTrue(form.fields["doctor"].disabled)


class DoctorScheduleFormTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.category = ServiceCategory.objects.create(
            name='Основные услуги',
            slug='main-services'
        )
        cls.service = Service.objects.create(
            name='Консультация',
            slug='consultation',
            category=cls.category,
            price=1000,
            duration=timedelta(minutes=30)
        )
        cls.doctor_user = User.objects.create_user(
            username='doctor',
            password='testpass123',
            email='doctor@example.com',
            is_doctor=True
        )
        cls.doctor = DoctorProfile.objects.create(
            user=cls.doctor_user,
            specialty='Кардиолог'
        )

    def get_valid_form_data(self, **overrides):
        """Генерирует валидные данные формы"""
        data = {
            "working_days": ["1", "2", "3"],
            "working_hours_start": "09:00",
            "working_hours_end": "17:00",
            "breaks": "[]",
            "vacation_dates": "[]",
        }
        data.update(overrides)
        return data

    def test_form_validation_valid_data(self):
        """Тест валидации с корректными данными"""
        form_data = {
            'working_days': ['1', '2', '3'],
            'working_hours_start': '09:00',
            'working_hours_end': '17:00',
            'breaks': '[]',
            'vacation_dates': '[]'
        }
        form = DoctorScheduleForm(data=form_data)
        self.assertTrue(form.is_valid(), f"Form errors: {form.errors}")

    def test_form_save(self):
        """Тест сохранения формы"""
        form = DoctorScheduleForm(data=self.get_valid_form_data())
        self.assertTrue(form.is_valid(), form.errors)

        schedule = form.save(commit=False)
        schedule.doctor = self.doctor
        schedule.save()

        self.assertEqual(schedule.working_days, [1, 2, 3])
        self.assertEqual(schedule.working_hours, {"start": "09:00", "end": "17:00"})
        self.assertEqual(schedule.breaks, [])
        self.assertEqual(schedule.vacation_dates, [])

    def test_invalid_time_range(self):
        """Тест неверного временного диапазона"""
        form = DoctorScheduleForm(
            data=self.get_valid_form_data(working_hours_start="18:00", working_hours_end="09:00")
        )
        self.assertFalse(form.is_valid())
        self.assertIn("working_hours_end", form.errors)

    def test_form_without_instance(self):
        """Тест формы без существующего экземпляра"""

        def _test():
            form = DoctorScheduleForm(data=self.get_valid_form_data())
            self.assertTrue(form.is_valid(), form.errors)
            schedule = form.save(commit=False)
            schedule.doctor = self.doctor
            schedule.save()
            self.assertEqual(schedule.working_hours, {'start': '09:00', 'end': '17:00'})

        transaction.on_commit(_test)
