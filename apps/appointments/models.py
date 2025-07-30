from django.contrib.postgres.fields import ArrayField
from django.db import models

from apps.services.models import Service
from apps.users.models import DoctorProfile, User


class Appointment(models.Model):
    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("confirmed", "Confirmed"),
        ("completed", "Completed"),
        ("cancelled", "Cancelled"),
    ]

    patient = models.ForeignKey(User, on_delete=models.CASCADE)
    doctor = models.ForeignKey(DoctorProfile, on_delete=models.CASCADE)
    service = models.ForeignKey(Service, on_delete=models.CASCADE, related_name="appointments")
    appointment_date = models.DateTimeField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="pending")
    notes = models.TextField(blank=True)
    results = models.FileField(upload_to="results/", blank=True, null=True)

    @property
    def results_url(self):
        return self.results.url if self.results else None


class DoctorSchedule(models.Model):
    doctor = models.OneToOneField(DoctorProfile, on_delete=models.CASCADE, related_name="schedule")
    working_days = ArrayField(models.IntegerField(), default=list, help_text="Дни недели (0-6, где 0 - понедельник)")
    working_hours = models.JSONField(default=dict, help_text='{"start": "09:00", "end": "18:00"}')
    breaks = models.JSONField(default=list, help_text='[{"start": "13:00", "end": "14:00"}]')
    vacation_dates = models.JSONField(default=list, help_text='[{"start": "2023-08-01", "end": "2023-08-14"}]')

    class Meta:
        verbose_name = "Расписание врача"
        verbose_name_plural = "Расписания врачей"

    def __str__(self):
        return f"Расписание {self.doctor.user.get_full_name()}"
