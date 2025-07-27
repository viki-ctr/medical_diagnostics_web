from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

User = get_user_model()


class AuthTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123',
            is_patient=True
        )

    def test_login_view(self):
        response = self.client.get(reverse('accounts:login'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/login.html')

        # Тест успешной авторизации
        login_response = self.client.post(reverse('accounts:login'), {
            'username': 'testuser',
            'password': 'testpass123'
        }, follow=True)
        self.assertTrue(login_response.context['user'].is_authenticated)

        # Тест редиректа после авторизации
        self.assertRedirects(login_response, reverse('core:home'))

    def test_register_view(self):
        response = self.client.get(reverse('accounts:register'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/register.html')

        # Тест успешной регистрации
        register_response = self.client.post(reverse('accounts:register'), {
            'username': 'newuser',
            'email': 'new@example.com',
            'password1': 'complexpassword123',
            'password2': 'complexpassword123',
            'is_patient': True
        }, follow=True)

        self.assertTrue(User.objects.filter(username='newuser').exists())
        self.assertRedirects(register_response, reverse('core:home'))
