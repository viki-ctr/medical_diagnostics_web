from django.contrib.auth import views as auth_views
from django.urls import path

from . import views

app_name = "users"


urlpatterns = [
    path("register/", views.RegisterView.as_view(), name="register"),
    path("login/", views.LoginView.as_view(), name="login"),
    path("logout/", views.LogoutView.as_view(), name="logout"),
    path("profile/", views.ProfileView.as_view(), name="profile"),
    path("password/change-password/", views.ChangePasswordView.as_view(), name="change-password"),
    path(
        "password/change-done/",
        auth_views.PasswordChangeDoneView.as_view(template_name="users/change_password_done.html"),
        name="change-password-done",
    ),
    path("profile/patient_profile/", views.PatientProfileView.as_view(), name="patient-profile"),
    path("profile/doctor_profile/", views.DoctorProfileView.as_view(), name="doctor-profile"),
    path("profile/update/", views.ProfileUpdateView.as_view(), name="profile-update"),
]
