from datetime import date, timedelta

import pytest
from django.core.files.uploadedfile import SimpleUploadedFile
from django.utils import timezone
from factory import Faker as FactoryFaker
from factory import SubFactory, fuzzy, post_generation
from factory.django import DjangoModelFactory

from apps.appointments.models import Appointment, DoctorSchedule
from apps.services.models import Service, ServiceCategory
from apps.users.models import DoctorProfile, PatientProfile, User


class ServiceCategoryFactory(DjangoModelFactory):
    class Meta:
        model = ServiceCategory

    name = FactoryFaker("word")
    slug = FactoryFaker("slug")
    description = FactoryFaker("text")


class ServiceFactory(DjangoModelFactory):
    class Meta:
        model = Service

    category = SubFactory(ServiceCategoryFactory)
    name = FactoryFaker("word")
    slug = FactoryFaker("slug")
    description = FactoryFaker("text")
    price = fuzzy.FuzzyDecimal(100.0, 10000.0)
    duration = timedelta(minutes=30)
    is_available = True


class UserFactory(DjangoModelFactory):
    class Meta:
        model = User

    username = FactoryFaker("user_name")
    email = FactoryFaker("email")
    first_name = FactoryFaker("first_name")
    last_name = FactoryFaker("last_name")
    is_doctor = True

    @post_generation
    def set_password(self, create, extracted, **kwargs):
        self.set_password("testpass123")


class PatientProfileFactory(DjangoModelFactory):
    class Meta:
        model = PatientProfile

    user = SubFactory(UserFactory, is_patient=True, is_doctor=False)
    birth_date = fuzzy.FuzzyDate(date(1950, 1, 1), date(2000, 1, 1))
    address = FactoryFaker("address")


class DoctorProfileFactory(DjangoModelFactory):
    class Meta:
        model = DoctorProfile

    user = SubFactory(UserFactory, is_doctor=True, is_patient=False)
    specialty = fuzzy.FuzzyChoice(["Cardiology", "Neurology", "Pediatrics"])
    bio = FactoryFaker("text", max_nb_chars=500)


class AppointmentFactory(DjangoModelFactory):
    class Meta:
        model = Appointment

    @classmethod
    def _create(cls, model_class, *args, **kwargs):
        if "patient" not in kwargs:
            patient_profile = PatientProfileFactory()
            kwargs["patient"] = patient_profile.user
        return super()._create(model_class, *args, **kwargs)

    doctor = SubFactory(DoctorProfileFactory)
    service = SubFactory(ServiceFactory)
    status = "pending"
    notes = FactoryFaker("text")
    appointment_date = fuzzy.FuzzyDateTime(
        start_dt=timezone.now() + timedelta(days=1), end_dt=timezone.now() + timedelta(days=30)
    )


class DoctorScheduleFactory(DjangoModelFactory):
    class Meta:
        model = DoctorSchedule

    doctor = SubFactory(DoctorProfileFactory)
    working_days = [0, 1, 2, 3, 4]
    working_hours = {"start": "09:00", "end": "18:00"}


@pytest.mark.django_db
def test_appointment_creation():
    """Тест создания записи на прием"""
    appointment = AppointmentFactory()
    assert appointment.pk is not None
    assert appointment.status == "pending"
    assert appointment.patient.is_patient
    assert appointment.doctor.user.is_doctor
    assert appointment.service.price > 0


@pytest.mark.django_db
def test_results_url_property():
    """Тест свойства results_url"""
    appointment = AppointmentFactory(results=None)
    assert appointment.results_url is None

    test_file = SimpleUploadedFile("test.txt", b"test content")
    appointment = AppointmentFactory(results=test_file)
    assert appointment.results_url is not None


@pytest.mark.django_db
def test_service_str():
    """Тест строкового представления услуги"""
    service = ServiceFactory()
    assert service.name in str(service)


@pytest.mark.django_db
def test_doctor_schedule_creation():
    """Тест создания расписания врача"""
    schedule = DoctorScheduleFactory()
    assert schedule.pk is not None
    assert schedule.doctor.specialty in ["Cardiology", "Neurology", "Pediatrics"]
