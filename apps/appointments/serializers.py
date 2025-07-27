from rest_framework import serializers
from apps.services.serializers import ServiceSerializer
from apps.users.serializers import DoctorProfileSerializer
from .models import Appointment

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

    def get_results_url(self, obj):
        if obj.results:
            return obj.results.url
        return None

    def validate_appointment_date(self, value):
        if value < timezone.now():
            raise serializers.ValidationError("Дата приема не может быть в прошлом")
        return value
