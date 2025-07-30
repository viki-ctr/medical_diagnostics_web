from django.urls import include, path
from rest_framework.routers import DefaultRouter

from . import views
from .views import (ChangePasswordAPIView, CurrentUserAPIView, CustomTokenObtainPairView,
                    DoctorProfileViewSet, LoginView, LogoutAPIView, LogoutView,
                    PatientProfileViewSet, ProfileView, RegisterAPIView, RegisterView)

app_name = "users"

router = DefaultRouter()
router.register(r"patients", PatientProfileViewSet, basename="patient")
router.register(r"doctors", DoctorProfileViewSet, basename="doctor")

urlpatterns = [

    path("api/register/", RegisterAPIView.as_view(), name="register"),
    path("api/login/", CustomTokenObtainPairView.as_view(), name="login"),
    path("api/me/", CurrentUserAPIView.as_view(), name="current-user"),
    path("api/change-password/", ChangePasswordAPIView.as_view(), name="change-password"),
    path("api/logout/", LogoutAPIView.as_view(), name="logout"),
    path("api/", include(router.urls)),

    path("login/", LoginView.as_view(), name="login-view"),
    path("register/", RegisterView.as_view(), name="register-view"),
    path("profile/", views.ProfileView.as_view(), name="profile-view"),
    path("change-password/", views.ChangePasswordView.as_view(), name="change-password-view"),
    path("logout/", LogoutView.as_view(), name="logout-view"),
    path("patients/<int:pk>/", views.PatientProfileView.as_view(), name="patient-profile-view"),
    path("doctors/<int:pk>/", views.DoctorProfileView.as_view(), name="doctor-profile-view"),

    path("", ProfileView.as_view(), name="user-home"),
]
