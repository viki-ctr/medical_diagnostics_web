from django.urls import path
from rest_framework.routers import DefaultRouter
from .api.views import (
    ServiceViewSet,
    ServiceCategoryViewSet,
    PopularServicesAPIView,
    DoctorServicesAPIView
)

router = DefaultRouter()
router.register(r'services', ServiceViewSet, basename='service')
router.register(r'categories', ServiceCategoryViewSet, basename='category')

urlpatterns = [
    path('popular/',
         PopularServicesAPIView.as_view(),
         name='popular-services'),
    path('doctors/<int:doctor_id>/services/',
         DoctorServicesAPIView.as_view(),
         name='doctor-services'),
] + router.urls
