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
    path('password-reset/',
         auth_views.PasswordResetView.as_view(
             template_name='users/password/reset.html'
         ),
         name='password_reset'),
    path('password-reset/done/',
         auth_views.PasswordResetDoneView.as_view(
             template_name='users/password/reset_done.html'
         ),
         name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(
             template_name='users/password/reset_confirm.html'
         ),
         name='password_reset_confirm'),
    path('password-reset-complete/',
         auth_views.PasswordResetCompleteView.as_view(
             template_name='users/password/reset_complete.html'
         ),
         name='password_reset_complete'),
]
