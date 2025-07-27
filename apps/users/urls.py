from django.urls import path
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from .views import (
    UserViewSet,
    PatientProfileViewSet,
    DoctorProfileViewSet,
    CurrentUserAPIView,
    RegisterAPIView,
    ChangePasswordAPIView
)

router = DefaultRouter()
router.register(r'patients', PatientProfileViewSet, basename='patient')
router.register(r'doctors', DoctorProfileViewSet, basename='doctor')

urlpatterns = [
    path('register/', RegisterAPIView.as_view(), name='register'),
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('me/', CurrentUserAPIView.as_view(), name='current-user'),
    path('change-password/', ChangePasswordAPIView.as_view(), name='change-password'),
    path('users/', UserViewSet.as_view({'get': 'list'}), name='user-list'),
] + router.urls
