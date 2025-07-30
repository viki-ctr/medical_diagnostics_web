from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    is_patient = models.BooleanField(default=False)
    is_doctor = models.BooleanField(default=False)
    phone = models.CharField(max_length=20, blank=True)

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"
        swappable = "AUTH_USER_MODEL"


class PatientProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    birth_date = models.DateField(null=True, blank=True)
    address = models.TextField(blank=True)
    medical_history = models.TextField(blank=True)


class DoctorProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    specialty = models.CharField(max_length=100)
    bio = models.TextField(blank=True)
    education = models.TextField(blank=True)
    experience = models.TextField(blank=True)
