from django.test import SimpleTestCase
from django.urls import reverse, resolve

from apps.appointments.views import AppointmentListView, AppointmentCreateView, DoctorScheduleView, AvailableSlotsView


class TestAppointmentsUrls(SimpleTestCase):
    def test_list_url_resolves(self):
        """Проверка URL списка записей"""
        url = reverse("appointments:list")
        self.assertEqual(resolve(url).func.view_class, AppointmentListView)
        self.assertEqual(url, "/appointments/")

    def test_create_url_resolves(self):
        """Проверка URL создания записи"""
        url = reverse("appointments:create")
        self.assertEqual(resolve(url).func.view_class, AppointmentCreateView)
        self.assertEqual(url, "/appointments/create/")

    def test_doctor_schedule_url_resolves(self):
        """Проверка URL расписания врача"""
        url = reverse("appointments:doctor-schedule", kwargs={"doctor_id": 1})
        self.assertEqual(resolve(url).func.view_class, DoctorScheduleView)
        self.assertEqual(url, "/appointments/doctors/1/schedule/")

    def test_available_slots_url_resolves(self):
        """Проверка URL доступных слотов"""
        url = reverse("appointments:available-slots")
        self.assertEqual(resolve(url).func.view_class, AvailableSlotsView)
        self.assertEqual(url, "/appointments/available-slots/")

    def test_url_namespaces(self):
        """Проверка namespace и app_name"""
        self.assertEqual(resolve("/appointments/").namespace, "appointments")
        self.assertEqual(resolve("/appointments/create/").app_name, "appointments")
