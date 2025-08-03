import json
from datetime import datetime, time, timedelta

from django.contrib.auth import get_user_model
from django.test import RequestFactory, TestCase
from django.urls import reverse
from django.utils import timezone

from apps.services.models import Service, ServiceCategory
from apps.users.models import DoctorProfile

from ..forms import AppointmentForm
from ..models import Appointment, DoctorSchedule
from ..views import AvailableSlotsView

User = get_user_model()


class AppointmentListViewTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.patient = User.objects.create_user(username="patient", email="patient@example.com", password="testpass")
        self.doctor_user = User.objects.create_user(
            username="doctor",
            email="doctor@example.com",
            password="testpass",
            is_staff=True,
        )
        self.doctor = DoctorProfile.objects.create(user=self.doctor_user)
        self.doctor_user.refresh_from_db()

        self.category = ServiceCategory.objects.create(name="General")
        self.service = Service.objects.create(
            name="Consultation", duration=timedelta(minutes=30), price=1000, category=self.category
        )

        self.appointment = Appointment.objects.create(
            patient=self.patient,
            doctor=self.doctor,
            service=self.service,
            appointment_date=timezone.now() + timedelta(days=1),
        )

    def test_patient_sees_own_appointments(self):
        self.client.force_login(self.patient)
        response = self.client.get(reverse("appointments:list"))
        self.assertEqual(response.status_code, 200)
        self.assertIn("appointments", response.context)
        appointments = response.context["appointments"]
        self.assertEqual(list(appointments), [self.appointment])
        self.assertEqual(appointments[0].patient, self.patient)

    def test_doctor_sees_own_appointments(self):
        self.client.force_login(self.doctor_user)

        for i in range(1, 3):
            Appointment.objects.create(
                doctor=self.doctor,
                patient=self.patient,
                service=self.service,
                appointment_date=timezone.now() + timedelta(days=i)
            )

        other_doctor = DoctorProfile.objects.create(
            user=User.objects.create_user(username='other_doctor', password='testpass')
        )
        Appointment.objects.create(
            doctor=other_doctor,
            patient=self.patient,
            service=self.service,
            appointment_date=timezone.now() + timedelta(days=3)
        )

        response = self.client.get(reverse('appointments:list'))
        self.assertEqual(response.status_code, 200)

        appointments = response.context['appointments']
        doctor_appointments = [a for a in appointments if a.doctor == self.doctor]
        self.assertEqual(len(doctor_appointments), 2)


class AppointmentCreateViewTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.patient = User.objects.create_user(username="patient", email="patient@example.com", password="testpass")
        self.doctor_user = User.objects.create_user(username="doctor", email="doctor@example.com", password="testpass")
        self.doctor = DoctorProfile.objects.create(user=self.doctor_user)

        self.category = ServiceCategory.objects.create(name="General")
        self.service = Service.objects.create(
            name="Consultation", duration=timedelta(minutes=30), price=1000, category=self.category
        )

        DoctorSchedule.objects.create(
            doctor=self.doctor, working_days=[1, 2, 3, 4, 5], working_hours={"start": "09:00", "end": "18:00"}
        )

    def test_get_create_form(self):
        self.client.force_login(self.patient)
        response = self.client.get(reverse("appointments:create"))
        self.assertEqual(response.status_code, 200)
        self.assertIn("form", response.context)
        form = response.context["form"]
        self.assertIsInstance(form, AppointmentForm)
        self.assertEqual(form.fields["doctor"].queryset.count(), DoctorProfile.objects.count())

    def test_post_create_appointment(self):
        self.client.force_login(self.patient)
        appointment_date = timezone.now() + timedelta(days=1)
        data = {
            "doctor": self.doctor.id,
            "service": self.service.id,
            "appointment_date": appointment_date.strftime("%Y-%m-%dT%H:%M"),
            "notes": "Test notes",
        }
        response = self.client.post(reverse("appointments:create"), data)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(
            Appointment.objects.filter(patient=self.patient, doctor=self.doctor, service=self.service).exists()
        )


class DoctorScheduleViewTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.doctor_user = User.objects.create_user(username="doctor", email="doctor@example.com", password="testpass")
        self.doctor = DoctorProfile.objects.create(user=self.doctor_user)

    def test_get_schedule_creates_if_not_exists(self):
        self.client.force_login(self.doctor_user)
        DoctorSchedule.objects.filter(doctor=self.doctor).delete()
        response = self.client.get(reverse("appointments:doctor-schedule", kwargs={"doctor_id": self.doctor.id}))
        self.assertEqual(response.status_code, 200)
        self.assertTrue(DoctorSchedule.objects.filter(doctor=self.doctor).exists())

    def test_post_updates_schedule(self):
        self.client.force_login(self.doctor_user)

        print(f"Doctor profile exists: {hasattr(self.doctor_user, 'doctor_profile')}")

        schedule = DoctorSchedule.objects.create(
            doctor=self.doctor, working_days=[1, 2, 3], working_hours={"start": "09:00", "end": "17:00"}
        )

        data = {
            "working_days": [1, 2, 3],
            "working_hours_start": "08:00",
            "working_hours_end": "18:00",
            "breaks": json.dumps([]),
            "vacation_dates": json.dumps([]),
        }

        response = self.client.post(
            reverse("appointments:doctor-schedule", kwargs={"doctor_id": self.doctor.id}), data, follow=True
        )

        if hasattr(response, "context") and "form" in response.context:
            print("Form errors:", response.context["form"].errors)

        schedule.refresh_from_db()
        print("Updated schedule:", schedule.__dict__)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(sorted(schedule.working_days), [1, 2, 3])
        self.assertEqual(schedule.working_hours, {"start": "08:00", "end": "18:00"})


class AvailableSlotsViewTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.patient = User.objects.create_user(username="patient", email="patient@example.com", password="testpass")
        self.doctor_user = User.objects.create_user(username="doctor", email="doctor@example.com", password="testpass")
        self.doctor = DoctorProfile.objects.create(user=self.doctor_user)

        self.category = ServiceCategory.objects.create(name="General")
        self.service = Service.objects.create(
            name="Consultation", duration=timedelta(minutes=30), price=1000, category=self.category
        )

        self.schedule = DoctorSchedule.objects.create(
            doctor=self.doctor, working_days=[1], working_hours={"start": "09:00", "end": "18:00"}
        )

        self.test_date = (timezone.now() + timedelta(days=(7 - timezone.now().weekday()))).date()
        self.date_str = self.test_date.strftime("%Y-%m-%d")

    def test_get_available_slots(self):
        url = reverse("appointments:available-slots")
        request = self.factory.get(url, {"doctor": self.doctor.id, "service": self.service.id, "date": self.date_str})
        request.user = self.patient
        response = AvailableSlotsView.as_view()(request)
        self.assertEqual(response.status_code, 200)
        response_data = json.loads(response.content)
        self.assertIn("slots", response_data)

    def test_missing_parameters(self):
        url = reverse("appointments:available-slots")
        request = self.factory.get(url)
        request.user = self.patient
        response = AvailableSlotsView.as_view()(request)
        self.assertEqual(response.status_code, 400)
        response_data = json.loads(response.content)
        self.assertEqual(response_data, {"error": "Missing required parameters"})

    def test_no_slots_on_non_working_day(self):
        self.schedule.working_days = [2]
        self.schedule.save()

        url = reverse("appointments:available-slots")
        request = self.factory.get(url,
                                   {"doctor": self.doctor.id, "service": self.service.id, "date": self.date_str})
        request.user = self.patient
        response = AvailableSlotsView.as_view()(request)
        self.assertEqual(response.status_code, 200)
        response_data = json.loads(response.content)
        self.assertEqual(len(response_data.get("slots", [])), 0)

    def test_slots_consider_existing_appointments(self):
        appointment_time = timezone.make_aware(datetime.combine(self.test_date, time(10, 0)))
        Appointment.objects.create(
            patient=self.patient, doctor=self.doctor, service=self.service, appointment_date=appointment_time
        )

        url = reverse("appointments:available-slots")
        request = self.factory.get(url,
                                   {"doctor": self.doctor.id, "service": self.service.id, "date": self.date_str})
        request.user = self.patient
        response = AvailableSlotsView.as_view()(request)
        self.assertEqual(response.status_code, 200)
        response_data = json.loads(response.content)
        self.assertNotIn("10:00", response_data.get("slots", []))
