from django.test import TestCase
from django.contrib.auth import get_user_model

from apps.core.models import AboutPage, Department, TeamMember, HomePageContent, Testimonial, FAQCategory, FAQ, \
    SiteSetting

User = get_user_model()


class AboutPageModelTest(TestCase):
    def setUp(self):
        self.about_page = AboutPage.objects.create(
            title="О нашей клинике",
            content="Основной контент о клинике",
            mission="Наша миссия",
            values="забота, эффективность, отзывчивость",
            is_active=True
        )

    def test_about_page_creation(self):
        self.assertEqual(self.about_page.title, "О нашей клинике")
        self.assertTrue(self.about_page.is_active)

    def test_values_as_list_method(self):
        values_list = self.about_page.values_as_list()
        self.assertEqual(len(values_list), 3)
        self.assertIn("забота", values_list)

    def test_only_one_active_page(self):
        new_page = AboutPage.objects.create(
            title="Новая страница",
            content="Контент",
            mission="Миссия",
            values="ценности",
            is_active=True
        )
        self.about_page.refresh_from_db()
        self.assertFalse(self.about_page.is_active)
        self.assertTrue(new_page.is_active)

    def test_string_representation(self):
        self.assertEqual(str(self.about_page), "О нашей клинике")


class DepartmentModelTest(TestCase):
    def setUp(self):
        self.department = Department.objects.create(
            name="Кардиология",
            description="Отделение кардиологии"
        )

    def test_department_creation(self):
        self.assertEqual(self.department.name, "Кардиология")
        self.assertEqual(self.department.description, "Отделение кардиологии")

    def test_string_representation(self):
        self.assertEqual(str(self.department), "Кардиология")


class TeamMemberModelTest(TestCase):
    def setUp(self):
        self.department = Department.objects.create(name="Неврология")
        self.user = User.objects.create_user(username="doctor", email="doctor@example.com", password="testpass123")
        self.team_member = TeamMember.objects.create(
            user=self.user,
            name="Иванов Иван",
            position="Главный врач",
            department=self.department,
            bio="Биография врача",
            order=1
        )

    def test_team_member_creation(self):
        self.assertEqual(self.team_member.name, "Иванов Иван")
        self.assertEqual(self.team_member.position, "Главный врач")
        self.assertEqual(self.team_member.department.name, "Неврология")

    def test_string_representation(self):
        self.assertEqual(str(self.team_member), "Иванов Иван - Главный врач")

    def test_ordering(self):
        TeamMember.objects.create(name="Петров Петр", position="Врач", department=self.department, order=0)
        first_member = TeamMember.objects.first()
        self.assertEqual(first_member.name, "Петров Петр")


class HomePageContentModelTest(TestCase):
    def setUp(self):
        self.home_content = HomePageContent.objects.create(
            main_title="Добро пожаловать",
            main_description="Описание клиники",
            services_title="Наши услуги",
            testimonials_title="Отзывы пациентов",
            is_active=True
        )

    def test_home_content_creation(self):
        self.assertEqual(self.home_content.main_title, "Добро пожаловать")
        self.assertTrue(self.home_content.is_active)

    def test_only_one_active_content(self):
        new_content = HomePageContent.objects.create(
            main_title="Новый заголовок",
            main_description="Новое описание",
            is_active=True
        )
        self.home_content.refresh_from_db()
        self.assertFalse(self.home_content.is_active)
        self.assertTrue(new_content.is_active)

    def test_get_testimonials_title(self):
        self.assertEqual(self.home_content.get_testimonials_title(), "Отзывы пациентов")

    def test_string_representation(self):
        self.assertIn("Конфигурация главной страницы", str(self.home_content))


class TestimonialModelTest(TestCase):
    def setUp(self):
        self.testimonial = Testimonial.objects.create(
            author="Пациент",
            content="Отличный сервис",
            rating=5,
            is_featured=True
        )

    def test_testimonial_creation(self):
        self.assertEqual(self.testimonial.author, "Пациент")
        self.assertEqual(self.testimonial.rating, 5)
        self.assertTrue(self.testimonial.is_featured)

    def test_stars_method(self):
        self.assertEqual(self.testimonial.stars(), "★★★★★")

    def test_get_short_content(self):
        self.assertEqual(self.testimonial.get_short_content(), "Отличный сервис")
        long_content = "Очень длинный отзыв " * 10
        testimonial = Testimonial.objects.create(author="Тест", content=long_content)
        self.assertTrue(len(testimonial.get_short_content()) <= 103)

    def test_string_representation(self):
        self.assertEqual(str(self.testimonial), "Отзыв от Пациент")


class FAQCategoryModelTest(TestCase):
    def setUp(self):
        self.category = FAQCategory.objects.create(
            name="Общие вопросы",
            slug="general",
            description="Частые вопросы общего характера"
        )

    def test_category_creation(self):
        self.assertEqual(self.category.name, "Общие вопросы")
        self.assertEqual(self.category.slug, "general")

    def test_string_representation(self):
        self.assertEqual(str(self.category), "Общие вопросы")


class FAQModelTest(TestCase):
    def setUp(self):
        self.category = FAQCategory.objects.create(name="Оплата", slug="payment")
        self.faq = FAQ.objects.create(
            question="Как оплатить услуги?",
            answer="Оплата возможна наличными или картой",
            category=self.category,
            order=1
        )

    def test_faq_creation(self):
        self.assertEqual(self.faq.question, "Как оплатить услуги?")
        self.assertEqual(self.faq.category.name, "Оплата")

    def test_string_representation(self):
        self.assertEqual(str(self.faq), "Как оплатить услуги?")

    def test_ordering(self):
        FAQ.objects.create(question="Другой вопрос", answer="Ответ", category=self.category, order=0)
        first_faq = FAQ.objects.first()
        self.assertEqual(first_faq.question, "Другой вопрос")


class SiteSettingModelTest(TestCase):
    def setUp(self):
        self.settings = SiteSetting.objects.create(
            site_name="МедДиагностика",
            phone="+7 (123) 456-78-90",
            email="info@example.com",
            address="ул. Медицинская, 1",
            working_hours="Пн-Пт: 9:00-18:00"
        )

    def test_site_setting_creation(self):
        self.assertEqual(self.settings.site_name, "МедДиагностика")
        self.assertEqual(self.settings.phone, "+7 (123) 456-78-90")

    def test_only_one_settings_instance(self):
        SiteSetting.objects.all().delete()
        settings1 = SiteSetting.objects.create(
            site_name="Настройки 1",
            phone="123"
        )
        settings2 = SiteSetting.objects.create(
            site_name="Настройки 2",
            phone="456"
        )
        self.assertEqual(SiteSetting.objects.count(), 1)
        self.assertEqual(SiteSetting.objects.first().site_name, "Настройки 2")

    def test_string_representation(self):
        self.assertEqual(str(self.settings), "МедДиагностика")
