from django.urls import path

from .views import AppointmentCreateView, AppointmentListView, AvailableSlotsView, DoctorScheduleView

app_name = "appointments"

urlpatterns = [
    path("", AppointmentListView.as_view(), name="list"),
    path("create/", AppointmentCreateView.as_view(), name="create"),
    path("doctors/<int:doctor_id>/schedule/", DoctorScheduleView.as_view(), name="doctor-schedule"),
    path("available-slots/", AvailableSlotsView.as_view(), name="available-slots"),
]
