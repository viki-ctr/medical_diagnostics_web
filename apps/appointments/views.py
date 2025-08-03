from datetime import datetime, time

from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views import View

from apps.services.models import Service
from apps.users.models import DoctorProfile

from .forms import AppointmentForm, DoctorScheduleForm
from .models import Appointment, DoctorSchedule


class AppointmentListView(LoginRequiredMixin, View):
    def get(self, request):
        if hasattr(request.user, "doctor_profile"):
            # Для врачей - все их назначения
            appointments = Appointment.objects.filter(doctor=request.user.doctor_profile).select_related(
                "patient", "service"
            )
        else:
            # Для пациентов - только их назначения
            appointments = Appointment.objects.filter(patient=request.user).select_related("doctor", "service")

        return render(request, "appointments/list.html", {"appointments": appointments.order_by("appointment_date")})


class AppointmentCreateView(LoginRequiredMixin, View):
    def get(self, request):
        form = AppointmentForm(user=request.user)
        return render(request, "appointments/create.html", {"form": form})

    def post(self, request):
        form = AppointmentForm(request.POST, user=request.user)
        if form.is_valid():
            appointment = form.save(commit=False)
            appointment.patient = request.user
            appointment.save()
            return redirect("appointments:list")
        return render(request, "appointments/create.html", {"form": form})


class DoctorScheduleView(LoginRequiredMixin, View):
    def get(self, request, doctor_id):
        doctor = get_object_or_404(DoctorProfile, id=doctor_id)
        schedule, created = DoctorSchedule.objects.get_or_create(
            doctor=doctor,
            defaults={"working_days": [1, 2, 3, 4, 5], "working_hours": {"start": "09:00", "end": "18:00"}},
        )
        form = DoctorScheduleForm(instance=schedule)
        return render(request, "doctors/schedule.html", {"form": form, "doctor": doctor})

    def post(self, request, doctor_id):
        doctor = get_object_or_404(DoctorProfile, id=doctor_id)
        schedule = get_object_or_404(DoctorSchedule, doctor=doctor)
        form = DoctorScheduleForm(request.POST, instance=schedule)
        if form.is_valid():
            form.save()
            return redirect("appointments:doctor-schedule", doctor_id=doctor.id)
        return render(request, "doctors/schedule.html", {"form": form, "doctor": doctor})


class AvailableSlotsView(LoginRequiredMixin, View):
    def get(self, request):
        doctor_id = request.GET.get("doctor")
        service_id = request.GET.get("service")
        date_str = request.GET.get("date")

        if not all([doctor_id, service_id, date_str]):
            return JsonResponse({"error": "Missing required parameters"}, status=400)

        try:
            date = datetime.strptime(date_str, "%Y-%m-%d").date()

            doctor = DoctorProfile.objects.get(id=doctor_id)
            service = Service.objects.get(id=service_id)
            duration = service.duration

            schedule = DoctorSchedule.objects.filter(doctor=doctor).first()
            if not schedule:
                return JsonResponse({"slots": []})

            weekday = date.weekday()
            if weekday not in schedule.working_days:
                return JsonResponse({"slots": []})

            start_time = datetime.combine(date, time.fromisoformat(schedule.working_hours["start"]))
            end_time = datetime.combine(date, time.fromisoformat(schedule.working_hours["end"]))

            breaks = [(time.fromisoformat(b["start"]), time.fromisoformat(b["end"])) for b in schedule.breaks]

            slots = []
            current_time = start_time
            while current_time + duration <= end_time:
                slot_available = True

                slot_time = current_time.time()
                for break_start, break_end in breaks:
                    if break_start <= slot_time < break_end:
                        slot_available = False
                        break

                if slot_available:
                    overlapping_appointments = Appointment.objects.filter(
                        doctor=doctor,
                        appointment_date__date=date,
                        appointment_date__time__gte=slot_time,
                        appointment_date__time__lt=(datetime.combine(date, slot_time) + duration).time(),
                    )
                    if not overlapping_appointments.exists():
                        slots.append(slot_time.strftime("%H:%M"))

                current_time += duration

            return render(
                request,
                "appointments/slots_partial.html",
                {"slots": slots, "date": date_str, "doctor": doctor, "service": service},
            )

        except (ValueError, DoctorProfile.DoesNotExist, Service.DoesNotExist) as e:
            return JsonResponse({"error": str(e)}, status=400)
