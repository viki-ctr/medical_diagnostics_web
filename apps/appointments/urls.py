from django.urls import path
from rest_framework.routers import DefaultRouter

from .views import AppointmentViewSet, AvailableTimeSlotsAPIView, DoctorScheduleAPIView

router = DefaultRouter()
router.register(r"appointments", AppointmentViewSet, basename="appointments")

urlpatterns = [
    path("doctors/<int:pk>/schedule/", DoctorScheduleAPIView.as_view(), name="doctor-schedule"),
    path("available-slots/", AvailableTimeSlotsAPIView.as_view(), name="available-slots"),
] + router.urls
