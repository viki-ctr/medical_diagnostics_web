from django import forms
from django.core.exceptions import ValidationError

from apps.services.models import Service
from apps.users.models import DoctorProfile

from .models import Appointment, DoctorSchedule


class AppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ['doctor', 'service', 'appointment_date', 'notes']
        widgets = {
            'appointment_date': forms.DateTimeInput(
                attrs={
                    'type': 'datetime-local',
                    'class': 'form-control'
                },
                format='%Y-%m-%dT%H:%M'
            )
        }

    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['doctor'].queryset = DoctorProfile.objects.all()
        self.fields['service'].queryset = Service.objects.all()

        self.fields['appointment_date'].input_formats = ['%Y-%m-%dT%H:%M']

        if user and user.is_doctor:
            self.fields["doctor"].initial = user.doctor_profile
            self.fields["doctor"].disabled = True


class DoctorScheduleForm(forms.ModelForm):
    working_days = forms.TypedMultipleChoiceField(
        choices=[(i, day) for i, day in enumerate(["Пн", "Вт", "Ср", "Чт", "Пт", "Сб", "Вс"], 1)],
        widget=forms.CheckboxSelectMultiple,
        coerce=int,
        required=False,
    )
    working_hours_start = forms.TimeField(widget=forms.TimeInput(attrs={"type": "time"}), required=True)
    working_hours_end = forms.TimeField(widget=forms.TimeInput(attrs={"type": "time"}), required=True)
    breaks = forms.JSONField(required=False, initial=list, widget=forms.HiddenInput())
    vacation_dates = forms.JSONField(required=False, initial=list, widget=forms.HiddenInput())

    class Meta:
        model = DoctorSchedule
        fields = ["working_days", "working_hours_start", "working_hours_end", "breaks", "vacation_dates"]
        widgets = {
            'working_hours': forms.HiddenInput(),
            'breaks': forms.HiddenInput(),
            'vacation_dates': forms.HiddenInput()
        }

    def clean(self):
        cleaned_data = super().clean()
        start = cleaned_data.get("working_hours_start")
        end = cleaned_data.get("working_hours_end")

        if start and end and start >= end:
            raise ValidationError({"working_hours_end": "Время окончания должно быть позже времени начала"})

        return cleaned_data

    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.working_hours = {
            "start": self.cleaned_data["working_hours_start"].strftime("%H:%M"),
            "end": self.cleaned_data["working_hours_end"].strftime("%H:%M"),
        }
        if commit:
            instance.save()
        return instance
