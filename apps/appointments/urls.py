from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import (
    AppointmentViewSet,
    DoctorScheduleAPIView,
    AvailableTimeSlotsAPIView
)

router = DefaultRouter()
router.register(r'appointments', AppointmentViewSet, basename='appointment')

urlpatterns = [
    path('doctors/<int:doctor_id>/schedule/',
         DoctorScheduleAPIView.as_view(),
         name='doctor-schedule'),
    path('available-slots/',
         AvailableTimeSlotsAPIView.as_view(),
         name='available-slots'),
] + router.urls