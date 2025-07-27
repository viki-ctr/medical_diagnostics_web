from django.test import TestCase, Client
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile
from rest_framework import status

from .models import ServiceCategory, Service
from django.utils import timezone
from rest_framework.test import APITestCase, APIClient

from .serializers import ServiceCategorySerializer, ServiceSerializer


class ServiceCategoryModelTest(TestCase):
    def setUp(self):
        self.category = ServiceCategory.objects.create(
            name="Консультации",
            slug="consultations",
            description="Врачебные консультации"
        )

    def test_category_creation(self):
        self.assertEqual(self.category.name, "Консультации")
        self.assertEqual(self.category.slug, "consultations")
        self.assertTrue(isinstance(self.category, ServiceCategory))
        self.assertEqual(str(self.category), "Консультации")

    def test_category_verbose_names(self):
        self.assertEqual(ServiceCategory._meta.verbose_name, "Категория услуг")
        self.assertEqual(ServiceCategory._meta.verbose_name_plural, "Категории услуг")


class ServiceModelTest(TestCase):
    def setUp(self):
        self.category = ServiceCategory.objects.create(
            name="Анализы",
            slug="analyses"
        )
        self.service = Service.objects.create(
            category=self.category,
            name="Общий анализ крови",
            slug="blood-test",
            description="Полный анализ крови",
            price=1500.00,
            duration=timezone.timedelta(minutes=30),
            is_available=True
        )

    def test_service_creation(self):
        self.assertEqual(self.service.name, "Общий анализ крови")
        self.assertEqual(self.service.category.name, "Анализы")
        self.assertEqual(self.service.price, 1500.00)
        self.assertEqual(self.service.duration.total_seconds(), 1800)
        self.assertTrue(self.service.is_available)
        self.assertEqual(str(self.service), "Общий анализ крови")

    def test_service_verbose_names(self):
        self.assertEqual(Service._meta.verbose_name, "Услуга")
        self.assertEqual(Service._meta.verbose_name_plural, "Услуги")

    def test_service_image_upload(self):
        image = SimpleUploadedFile("test.jpg", b"file_content", content_type="image/jpeg")
        service = Service.objects.create(
            category=self.category,
            name="Тест с изображением",
            slug="test-image",
            description="Тест",
            price=1000,
            duration=timezone.timedelta(minutes=15),
            image=image
        )
        self.assertTrue(service.image.name.startswith('services/'))


class ServiceCategorySerializerTest(TestCase):
    def setUp(self):
        self.category = ServiceCategory.objects.create(
            name="Диагностика",
            slug="diagnostics"
        )
        Service.objects.create(
            category=self.category,
            name="МРТ",
            slug="mri",
            description="Магнитно-резонансная томография",
            price=5000,
            duration=timezone.timedelta(minutes=45)
        )

    def test_serializer_fields(self):
        serializer = ServiceCategorySerializer(instance=self.category)
        data = serializer.data
        self.assertEqual(data['name'], "Диагностика")
        self.assertEqual(data['services_count'], 1)


class ServiceSerializerTest(APITestCase):
    def setUp(self):
        self.category = ServiceCategory.objects.create(
            name="УЗИ",
            slug="ultrasound"
        )
        self.service = Service.objects.create(
            category=self.category,
            name="УЗИ брюшной полости",
            slug="abdominal-ultrasound",
            description="Ультразвуковое исследование",
            price=2500,
            duration=timezone.timedelta(minutes=30)
        )

    def test_serializer_fields(self):
        serializer = ServiceSerializer(instance=self.service)
        data = serializer.data
        self.assertEqual(data['name'], "УЗИ брюшной полости")
        self.assertEqual(data['category_name'], "УЗИ")
        self.assertEqual(data['duration_formatted'], "30 мин")
        self.assertEqual(data['price'], "2500.00")

    def test_image_url_serialization(self):
        serializer = ServiceSerializer(instance=self.service)
        self.assertIsNone(serializer.data['image_url'])


class ServiceListViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.category = ServiceCategory.objects.create(
            name="Терапия",
            slug="therapy"
        )
        self.service1 = Service.objects.create(
            category=self.category,
            name="Прием терапевта",
            slug="therapist",
            description="Консультация терапевта",
            price=2000,
            duration=timezone.timedelta(minutes=30)
        )
        self.service2 = Service.objects.create(
            category=self.category,
            name="Повторный прием",
            slug="therapist-repeat",
            description="Повторная консультация",
            price=1500,
            duration=timezone.timedelta(minutes=20)
        )

    def test_list_view(self):
        response = self.client.get(reverse('services:list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Прием терапевта")
        self.assertTemplateUsed(response, 'services/list.html')

    def test_list_view_with_category(self):
        url = reverse('services:list_by_category', kwargs={'category_slug': 'therapy'})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['services']), 2)


class ServiceDetailViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.category = ServiceCategory.objects.create(
            name="Хирургия",
            slug="surgery"
        )
        self.service = Service.objects.create(
            category=self.category,
            name="Удаление аппендикса",
            slug="appendectomy",
            description="Операция по удалению",
            price=30000,
            duration=timezone.timedelta(hours=1)
        )

    def test_detail_view(self):
        url = reverse('services:detail', kwargs={'slug': 'appendectomy'})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Удаление аппендикса")
        self.assertEqual(response.context['service'], self.service)


class ServiceViewSetTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.category = ServiceCategory.objects.create(
            name="Кардиология",
            slug="cardiology"
        )
        self.service = Service.objects.create(
            category=self.category,
            name="ЭКГ",
            slug="ecg",
            description="Электрокардиограмма",
            price=1200,
            duration=timezone.timedelta(minutes=15),
            is_available=True
        )

    def test_service_list(self):
        url = reverse('service-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['name'], "ЭКГ")

    def test_service_detail(self):
        url = reverse('service-detail', kwargs={'slug': 'ecg'})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], "ЭКГ")


class PopularServicesAPIViewTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.category = ServiceCategory.objects.create(name="Анализы", slug="tests")
        self.popular_service = Service.objects.create(
            category=self.category,
            name="Общий анализ крови",
            slug="blood-test",
            price=500,
            duration=timezone.timedelta(minutes=10),
            is_available=True
        )

    def test_popular_services(self):
        url = reverse('popular-services')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['name'], "Общий анализ крови")


class ServiceIntegrationTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.category = ServiceCategory.objects.create(
            name="Стоматология",
            slug="dentistry"
        )
        self.service1 = Service.objects.create(
            category=self.category,
            name="Чистка зубов",
            slug="teeth-cleaning",
            price=3000,
            duration=timezone.timedelta(minutes=45)
        )

    def test_full_flow(self):
        list_url = reverse('services:list')
        response = self.client.get(list_url)
        self.assertContains(response, "Стоматология")

        detail_url = reverse('services:detail', kwargs={'slug': 'teeth-cleaning'})
        response = self.client.get(detail_url)
        self.assertContains(response, "Чистка зубов")

        api_client = APIClient()
        api_url = reverse('service-list')
        response = api_client.get(api_url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data[0]['name'], "Чистка зубов")
