from rest_framework import serializers
from .models import DoctorSchedule, Appointment
from apps.services.models import Service
from django.utils import timezone

from ..services.serializers import ServiceSerializer
from ..users.models import DoctorProfile
from ..users.serializers import DoctorProfileSerializer


class AppointmentSerializer(serializers.ModelSerializer):
    service = ServiceSerializer(read_only=True)
    service_id = serializers.PrimaryKeyRelatedField(
        queryset=Service.objects.all(),
        write_only=True,
        source='service'
    )
    doctor = DoctorProfileSerializer(read_only=True)
    doctor_id = serializers.PrimaryKeyRelatedField(
        queryset=DoctorProfile.objects.all(),
        write_only=True,
        source='doctor'
    )
    patient_name = serializers.CharField(source='patient.get_full_name', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)

    class Meta:
        model = Appointment
        fields = [
            'id',
            'patient',
            'patient_name',
            'doctor',
            'doctor_id',
            'service',
            'service_id',
            'appointment_date',
            'status',
            'status_display',
            'notes',
            'results_url',
            'created_at'
        ]
        read_only_fields = ['patient', 'created_at']

    results_url = serializers.SerializerMethodField()

    def get_results_url(self, obj):
        return obj.results.url if obj.results else None

    def validate_appointment_date(self, value):
        if value < timezone.now():
            raise serializers.ValidationError("Дата приема не может быть в прошлом")
        return value


class DoctorScheduleSerializer(serializers.ModelSerializer):
    doctor_name = serializers.CharField(source='doctor.user.get_full_name', read_only=True)

    class Meta:
        model = DoctorSchedule
        fields = [
            'id',
            'doctor',
            'doctor_name',
            'working_days',
            'working_hours',
            'breaks',
            'vacation_dates'
        ]


class AvailableTimeSlotsSerializer(serializers.Serializer):
    doctor = serializers.PrimaryKeyRelatedField(queryset=DoctorProfile.objects.all())
    service = serializers.PrimaryKeyRelatedField(queryset=Service.objects.all())
    date = serializers.DateField()

    def validate(self, data):
        if data['date'] < timezone.now().date():
            raise serializers.ValidationError("Дата не может быть в прошлом")
        return data

    def to_representation(self, instance):
        doctor = instance['doctor']
        service = instance['service']
        date = instance['date']

        schedule = DoctorSchedule.objects.filter(doctor=doctor).first()
        if not schedule:
            return {'slots': []}

        appointments = Appointment.objects.filter(
            doctor=doctor,
            appointment_date__date=date
        ).values_list('appointment_date__time', flat=True)

        start_time = timezone.datetime.combine(
            date,
            timezone.datetime.strptime(schedule.working_hours['start'], '%H:%M').time()
        )
        end_time = timezone.datetime.combine(
            date,
            timezone.datetime.strptime(schedule.working_hours['end'], '%H:%M').time()
        )

        slots = []
        current_time = start_time
        while current_time + service.duration <= end_time:
            if current_time.time() not in appointments:
                slots.append(current_time.time().strftime('%H:%M'))
            current_time += service.duration

        return {
            'doctor': doctor.id,
            'service': service.id,
            'date': date,
            'slots': slots
        }
