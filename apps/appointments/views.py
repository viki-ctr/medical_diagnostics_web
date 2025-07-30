from django.utils import timezone
from rest_framework import generics, permissions, viewsets

from apps.services.models import Service
from apps.users.models import DoctorProfile

from .models import Appointment, DoctorSchedule
from .serializers import AppointmentSerializer, AvailableTimeSlotsSerializer, DoctorScheduleSerializer


class AppointmentViewSet(viewsets.ModelViewSet):
    """
    Управление записями на прием
    GET, POST /api/appointments/appointments/
    GET, PUT, DELETE /api/appointments/appointments/<id>/
    """

    serializer_class = AppointmentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.is_doctor:
            return Appointment.objects.filter(doctor=user.doctorprofile)
        elif user.is_patient:
            return Appointment.objects.filter(patient=user)
        return Appointment.objects.none()

    def perform_create(self, serializer):
        if self.request.user.is_patient:
            serializer.save(patient=self.request.user)


class DoctorScheduleAPIView(generics.RetrieveUpdateAPIView):
    """
    Управление расписанием врача
    GET, PUT /api/appointments/doctors/<doctor_id>/schedule/
    """

    queryset = DoctorSchedule.objects.all()
    serializer_class = DoctorScheduleSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        doctor_id = self.kwargs.get("doctor_id")
        schedule, created = DoctorSchedule.objects.get_or_create(
            doctor_id=doctor_id,
            defaults={"working_days": [1, 2, 3, 4, 5], "working_hours": {"start": "09:00", "end": "18:00"}},
        )
        return schedule


class AvailableTimeSlotsAPIView(generics.ListAPIView):
    """
    Получение доступных временных слотов
    GET /api/appointments/available-slots/?doctor=<id>&service=<id>&date=<YYYY-MM-DD>
    """

    serializer_class = AvailableTimeSlotsSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        doctor_id = self.request.query_params.get("doctor")
        service_id = self.request.query_params.get("service")
        date_str = self.request.query_params.get("date")

        if not all([doctor_id, service_id, date_str]):
            return []

        try:
            date = timezone.datetime.strptime(date_str, "%Y-%m-%d").date()
            doctor = DoctorProfile.objects.get(id=doctor_id)
            service = Service.objects.get(id=service_id)
            duration = service.duration
        except (ValueError, DoctorProfile.DoesNotExist, Service.DoesNotExist):
            return []

        schedule = DoctorSchedule.objects.filter(doctor=doctor).first()
        if not schedule:
            return []

        slots = []
        start_time = timezone.datetime.combine(date, schedule.working_hours["start"])
        end_time = timezone.datetime.combine(date, schedule.working_hours["end"])

        current_time = start_time
        while current_time + duration <= end_time:
            slots.append(current_time.time())
            current_time += duration

        return slots
