from django.test import SimpleTestCase
from django.urls import reverse, resolve
from django.contrib.auth import views as auth_views

from apps.users import views


class TestUsersUrls(SimpleTestCase):
    def test_register_url_resolves(self):
        url = reverse("users:register")
        self.assertEqual(resolve(url).func.view_class, views.RegisterView)
        self.assertEqual(url, "/users/register/")

    def test_login_url_resolves(self):
        url = reverse("users:login")
        self.assertEqual(resolve(url).func.view_class, views.LoginView)
        self.assertEqual(url, "/users/login/")

    def test_logout_url_resolves(self):
        url = reverse("users:logout")
        self.assertEqual(resolve(url).func.view_class, views.LogoutView)
        self.assertEqual(url, "/users/logout/")

    def test_profile_url_resolves(self):
        url = reverse("users:profile")
        self.assertEqual(resolve(url).func.view_class, views.ProfileView)
        self.assertEqual(url, "/users/profile/")

    def test_change_password_url_resolves(self):
        url = reverse("users:change-password")
        self.assertEqual(resolve(url).func.view_class, views.ChangePasswordView)
        self.assertEqual(url, "/users/password/change-password/")

    def test_change_password_done_url_resolves(self):
        url = reverse("users:change-password-done")
        self.assertEqual(resolve(url).func.view_class, auth_views.PasswordChangeDoneView)
        self.assertEqual(url, "/users/password/change-done/")

    def test_patient_profile_url_resolves(self):
        url = reverse("users:patient-profile")
        self.assertEqual(resolve(url).func.view_class, views.PatientProfileView)
        self.assertEqual(url, "/users/profile/patient_profile/")

    def test_doctor_profile_url_resolves(self):
        url = reverse("users:doctor-profile")
        self.assertEqual(resolve(url).func.view_class, views.DoctorProfileView)
        self.assertEqual(url, "/users/profile/doctor_profile/")

    def test_profile_update_url_resolves(self):
        url = reverse("users:profile-update")
        self.assertEqual(resolve(url).func.view_class, views.ProfileUpdateView)
        self.assertEqual(url, "/users/profile/update/")
