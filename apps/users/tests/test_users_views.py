from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from ..models import DoctorProfile, PatientProfile


User = get_user_model()


class RegisterViewTest(TestCase):
    def setUp(self):
        self.url = reverse('users:register')
        self.valid_data = {
            'username': 'testuser',
            'email': 'test@example.com',
            'password1': 'TestPass123!',
            'password2': 'TestPass123!'
        }

    def test_register_page_loads(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/register.html')

    def test_register_success(self):
        response = self.client.post(self.url, self.valid_data)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(User.objects.filter(username='testuser').exists())


class LoginViewTest(TestCase):
    def setUp(self):
        self.url = reverse('users:login')
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='TestPass123'
        )

    def test_login_page_loads(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/login.html')
        self.assertContains(response, 'Вход в систему')
        self.assertContains(response, 'name="username"')
        self.assertContains(response, 'name="password"')

    def test_login_success(self):
        response = self.client.post(self.url, {
            'username': 'testuser',
            'password': 'TestPass123'
        })
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('users:profile'))

    def test_login_invalid_credentials(self):
        response = self.client.post(self.url, {
            'username': 'testuser',
            'password': 'wrongpassword'
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Пожалуйста, введите правильные имя пользователя и пароль')

    def test_login_redirect_authenticated_user(self):
        self.client.login(username='testuser', password='TestPass123')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('users:profile'))

    def test_password_reset_link_exists(self):
        response = self.client.get(self.url)
        self.assertContains(response, reverse('users:password_reset'))


class LogoutViewTest(TestCase):
    def setUp(self):
        self.url = reverse('users:logout')
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.client.login(username='testuser', password='testpass123')

    def test_logout_view(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/logout.html')


class ProfileViewTest(TestCase):
    def setUp(self):
        self.url = reverse('users:profile')
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.patient_profile = PatientProfile.objects.create(user=self.user)
        self.client.login(username='testuser', password='testpass123')

    def test_profile_view(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/profile/profile.html')


class ChangePasswordViewTest(TestCase):
    def setUp(self):
        self.url = reverse('users:change-password')
        self.user = User.objects.create_user(
            username='testuser',
            password='oldpassword'
        )
        self.client.login(username='testuser', password='oldpassword')

    def test_password_change(self):
        response = self.client.post(self.url, {
            'old_password': 'oldpassword',
            'new_password1': 'newpassword123!',
            'new_password2': 'newpassword123!'
        })
        self.assertEqual(response.status_code, 302)
        self.user.refresh_from_db()
        self.assertTrue(self.user.check_password('newpassword123!'))


class PatientProfileViewTest(TestCase):
    def setUp(self):
        self.url = reverse('users:patient-profile')
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.profile = PatientProfile.objects.create(user=self.user)
        self.client.login(username='testuser', password='testpass123')

    def test_patient_profile_update(self):
        response = self.client.post(self.url, {
            'phone': '+79991234567',
            'birth_date': '2000-01-01'
        })
        self.assertEqual(response.status_code, 302)
        self.profile.refresh_from_db()
        self.assertEqual(self.profile.phone, '+79991234567')


class DoctorProfileViewTest(TestCase):
    def setUp(self):
        self.url = reverse('users:doctor-profile')
        self.user = User.objects.create_user(
            username='doctor',
            password='testpass123'
        )
        self.profile = DoctorProfile.objects.create(
            user=self.user,
            specialty='Cardiology',
            department='General'
        )
        self.client.login(username='doctor', password='testpass123')

    def test_doctor_profile_update(self):
        response = self.client.post(self.url, {
            'specialty': 'Neurology',
            'department': 'Neurology Department'
        })
        self.assertEqual(response.status_code, 302)
        self.profile.refresh_from_db()
        self.assertEqual(self.profile.specialty, 'Neurology')


class ProfileUpdateViewTest(TestCase):
    def setUp(self):
        self.url = reverse('users:profile-update')
        self.user = User.objects.create_user(
            username='testuser',
            email='old@example.com',
            password='testpass123'
        )
        self.client.login(username='testuser', password='testpass123')

    def test_profile_update(self):
        response = self.client.post(self.url, {
            'username': 'testuser',
            'email': 'new@example.com',
            'first_name': 'John',
            'last_name': 'Doe'
        })
        self.assertEqual(response.status_code, 302)
        self.user.refresh_from_db()
        self.assertEqual(self.user.email, 'new@example.com')
