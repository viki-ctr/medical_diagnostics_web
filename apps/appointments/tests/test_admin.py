from django.test import TestCase, RequestFactory
from django.contrib.admin.sites import AdminSite
from django.contrib.auth import get_user_model
from django.utils import timezone
from datetime import timedelta

from apps.appointments.admin import AppointmentAdmin, DoctorScheduleAdmin, SpecialtyFilter
from apps.appointments.models import Appointment, DoctorSchedule
from apps.services.models import ServiceCategory, Service
from apps.users.models import DoctorProfile

User = get_user_model()


class MockRequest:
    pass


class MockSuperUser:
    def has_perm(self, perm):
        return True


request = MockRequest()
request.user = MockSuperUser()


class AppointmentAdminTest(TestCase):
    def setUp(self):
        self.site = AdminSite()
        self.admin = AppointmentAdmin(Appointment, self.site)
        self.factory = RequestFactory()

        self.user_patient = User.objects.create_user(
            username='patient', email='patient@test.com', password='testpass123'
        )
        self.user_doctor = User.objects.create_user(
            username='doctor', email='doctor@test.com', password='testpass123'
        )
        self.doctor = DoctorProfile.objects.create(
            user=self.user_doctor, specialty='cardiologist'
        )
        self.category = ServiceCategory.objects.create(name="Консультации")
        self.service = Service.objects.create(
            name='Консультация',
            price=2000,
            duration=timedelta(minutes=30),
            category=self.category  # Добавляем категорию
        )
        self.appointment = Appointment.objects.create(
            patient=self.user_patient,
            doctor=self.doctor,
            service=self.service,
            appointment_date=timezone.now(),
            status='pending'
        )

    def test_list_display(self):
        self.assertEqual(
            self.admin.list_display,
            (
                "id",
                "patient_info",
                "doctor_info",
                "service_info",
                "appointment_date_formatted",
                "status",
                "results_link",
                "custom_actions",
            )
        )

    def test_patient_info(self):
        result = self.admin.patient_info(self.appointment)
        self.assertIn('href', result)
        self.assertIn(str(self.user_patient.id), result)
        self.assertIn(self.user_patient.username, result)

    def test_doctor_info(self):
        result = self.admin.doctor_info(self.appointment)
        self.assertIn(self.doctor.user.get_full_name(), result)
        self.assertIn(self.doctor.specialty, result)

    def test_service_info(self):
        result = self.admin.service_info(self.appointment)
        self.assertIn(self.service.name, result)
        self.assertIn(str(self.service.price), result)

    def test_appointment_date_formatted(self):
        result = self.admin.appointment_date_formatted(self.appointment)
        self.assertIsNotNone(result)

    def test_custom_actions(self):
        result = self.admin.custom_actions(self.appointment)
        self.assertIn('View', result)
        self.assertIn('Change', result)
        self.assertIn(str(self.appointment.id), result)

    def test_mark_as_confirmed_action(self):
        queryset = Appointment.objects.filter(pk=self.appointment.pk)
        self.admin.mark_as_confirmed(None, queryset)
        self.appointment.refresh_from_db()
        self.assertEqual(self.appointment.status, 'confirmed')

    def test_mark_as_completed_action(self):
        queryset = Appointment.objects.filter(pk=self.appointment.pk)
        self.admin.mark_as_completed(None, queryset)
        self.appointment.refresh_from_db()
        self.assertEqual(self.appointment.status, 'completed')

    def test_mark_as_cancelled_action(self):
        queryset = Appointment.objects.filter(pk=self.appointment.pk)
        self.admin.mark_as_cancelled(None, queryset)
        self.appointment.refresh_from_db()
        self.assertEqual(self.appointment.status, 'cancelled')

    def test_search_fields(self):
        self.assertEqual(
            self.admin.search_fields,
            ("patient__username", "patient__email", "doctor__user__username", "service__name")
        )

    def test_list_filter(self):
        self.assertEqual(
            len(self.admin.list_filter),
            5
        )


class DoctorScheduleAdminTest(TestCase):
    def setUp(self):
        self.site = AdminSite()
        self.admin = DoctorScheduleAdmin(DoctorSchedule, self.site)
        self.user_doctor = User.objects.create_user(
            username='doctor', email='doctor@test.com', password='testpass123'
        )
        self.doctor = DoctorProfile.objects.create(
            user=self.user_doctor, specialty='cardiologist'
        )
        self.schedule = DoctorSchedule.objects.create(
            doctor=self.doctor,
            working_days=[0, 1, 2],  # Пн, Вт, Ср
            working_hours={'start': '09:00', 'end': '18:00'}
        )

    def test_list_display(self):
        self.assertEqual(
            self.admin.list_display,
            ("doctor", "formatted_working_days", "working_hours_display")
        )

    def test_formatted_working_days(self):
        result = self.admin.formatted_working_days(self.schedule)
        self.assertEqual(result, "Пн, Вт, Ср")

    def test_working_hours_display(self):
        result = self.admin.working_hours_display(self.schedule)
        self.assertEqual(result, "09:00 - 18:00")


class SpecialtyFilterTest(TestCase):
    def setUp(self):
        self.original_choices = getattr(DoctorProfile, 'SPECIALTY_CHOICES', None)
        DoctorProfile.SPECIALTY_CHOICES = [
            ('cardiologist', 'Кардиолог'),
            ('neurologist', 'Невролог')
        ]

        self.user1 = User.objects.create_user(username='doctor1', password='test123')
        self.user2 = User.objects.create_user(username='doctor2', password='test123')

        self.doctor1 = DoctorProfile.objects.create(user=self.user1, specialty='cardiologist')
        self.doctor2 = DoctorProfile.objects.create(user=self.user2, specialty='neurologist')

        self.category = ServiceCategory.objects.create(name="Консультации")

        self.schedule1 = DoctorSchedule.objects.create(doctor=self.doctor1, working_days=[0, 1])
        self.schedule2 = DoctorSchedule.objects.create(doctor=self.doctor2, working_days=[2, 3])

    def tearDown(self):
        if self.original_choices is not None:
            DoctorProfile.SPECIALTY_CHOICES = self.original_choices
        else:
            delattr(DoctorProfile, 'SPECIALTY_CHOICES')

    def test_lookups(self):
        filter = SpecialtyFilter(None, {}, None, None)
        lookups = filter.lookups(None, None)
        self.assertEqual(lookups, DoctorProfile.SPECIALTY_CHOICES)
