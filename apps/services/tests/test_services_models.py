from django.test import TestCase
from apps.services.models import ServiceCategory, Service

class ServiceCategoryModelTest(TestCase):
    def test_create_category(self):
        category = ServiceCategory.objects.create(
            name="Анализы",
            slug="analizy",
            description="Медицинские анализы"
        )
        self.assertEqual(category.name, "Анализы")
        self.assertEqual(category.slug, "analizy")
        self.assertEqual(category.icon, "fa-flask")

class ServiceModelTest(TestCase):
    def setUp(self):
        self.category = ServiceCategory.objects.create(
            name="Анализы",
            slug="analizy",
            description="Медицинские анализы"
        )

    def test_create_service(self):
        service = Service.objects.create(
            category=self.category,
            name="Общий анализ крови",
            slug="obshiy-analiz-krovi",
            description="Описание",
            price=1000,
            duration="01:00:00"
        )
        self.assertEqual(service.name, "Общий анализ крови")
        self.assertEqual(service.category, self.category)
