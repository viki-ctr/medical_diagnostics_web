from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    is_patient = models.BooleanField(default=False)
    is_doctor = models.BooleanField(default=False)

    def __str__(self):
        return self.username


class PatientProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="patient_profile")
    birth_date = models.DateField(null=True, blank=True)
    GENDER_CHOICES = [
        ("M", "Мужской"),
        ("F", "Женский"),
        ("O", "Другой"),
    ]
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, blank=True)
    address = models.TextField(blank=True)
    phone = models.CharField(max_length=20, blank=True)
    medical_history = models.TextField(blank=True)

    def __str__(self):
        return f"Профиль пациента: {self.user.username}"


class DoctorProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="doctor_profile")
    specialty = models.CharField(max_length=100)
    department = models.CharField(max_length=100, default="Общее отделение", verbose_name="Отделение")
    bio = models.TextField(blank=True, null=True)
    def __str__(self):
        return f"Профиль врача: {self.user.username} ({self.specialty})"
