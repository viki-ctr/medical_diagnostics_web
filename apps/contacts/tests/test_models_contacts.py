import pytest
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase

from django.core.exceptions import ValidationError

from apps.contacts.models import ContactInfo, Feedback, Branch


class ContactInfoModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Создаем объект для тестирования
        ContactInfo.objects.create(
            address="ул. Тестовая, 123",
            phone="+79991234567",
            email="test@example.com",
            working_hours="09:00-18:00;Без перерыва",
            map_embed_code="<iframe>...</iframe>"
        )

    def test_address_field(self):
        contact = ContactInfo.objects.get(id=1)
        field = contact._meta.get_field('address')
        self.assertEqual(field.__class__.__name__, 'TextField')
        self.assertEqual(contact.address, "ул. Тестовая, 123")

    def test_phone_field(self):
        contact = ContactInfo.objects.get(id=1)
        field = contact._meta.get_field('phone')
        self.assertEqual(field.max_length, 20)
        self.assertEqual(contact.phone, "+79991234567")

    def test_email_field(self):
        contact = ContactInfo.objects.get(id=1)
        field = contact._meta.get_field('email')
        self.assertEqual(field.__class__.__name__, 'EmailField')

    def test_working_hours_field(self):
        contact = ContactInfo.objects.get(id=1)
        field = contact._meta.get_field('working_hours')
        self.assertEqual(field.max_length, 100)

    def test_map_embed_code_field(self):
        contact = ContactInfo.objects.get(id=1)
        field = contact._meta.get_field('map_embed_code')
        self.assertEqual(field.__class__.__name__, 'TextField')
        self.assertTrue(field.blank)

    def test_get_working_hours_list_method(self):
        contact = ContactInfo.objects.get(id=1)
        hours_list = contact.get_working_hours_list()
        self.assertEqual(hours_list, ["09:00-18:00", "Без перерыва"])

    def test_get_working_hours_list_empty(self):
        contact = ContactInfo.objects.create(
            address="ул. Тестовая, 123",
            phone="+79991234567",
            email="test@example.com",
            working_hours=""
        )
        self.assertEqual(contact.get_working_hours_list(), [])


class FeedbackModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        Feedback.objects.create(
            name="Иван Иванов",
            email="ivan@example.com",
            phone="+79991234567",
            subject="Тестовый вопрос",
            message="Это тестовое сообщение длиннее 50 символов, чтобы проверить метод get_short_message",
            is_processed=True
        )

    def test_name_field(self):
        feedback = Feedback.objects.get(id=1)
        field = feedback._meta.get_field('name')
        self.assertEqual(field.max_length, 100)
        self.assertEqual(feedback.name, "Иван Иванов")

    def test_email_field(self):
        feedback = Feedback.objects.get(id=1)
        field = feedback._meta.get_field('email')
        self.assertEqual(field.__class__.__name__, 'EmailField')

    def test_phone_field(self):
        feedback = Feedback.objects.get(id=1)
        field = feedback._meta.get_field('phone')
        self.assertEqual(field.max_length, 20)
        self.assertTrue(field.blank)

    def test_subject_field(self):
        feedback = Feedback.objects.get(id=1)
        field = feedback._meta.get_field('subject')
        self.assertEqual(field.max_length, 200)

    def test_message_field(self):
        feedback = Feedback.objects.get(id=1)
        field = feedback._meta.get_field('message')
        self.assertEqual(field.__class__.__name__, 'TextField')

    def test_created_at_field(self):
        feedback = Feedback.objects.get(id=1)
        field = feedback._meta.get_field('created_at')
        self.assertTrue(field.auto_now_add)

    def test_is_processed_field(self):
        feedback = Feedback.objects.get(id=1)
        field = feedback._meta.get_field('is_processed')
        self.assertFalse(field.default)
        self.assertTrue(feedback.is_processed)

    def test_get_short_message_method(self):
        feedback = Feedback.objects.get(id=1)
        expected_start = feedback.message[:50]
        short_message = feedback.get_short_message()

        if len(feedback.message) > 50:
            self.assertEqual(short_message, expected_start + "...")
        else:
            self.assertEqual(short_message, feedback.message)

    def test_get_short_message_short(self):
        feedback = Feedback.objects.create(
            name="Тест",
            email="test@example.com",
            subject="Тест",
            message="Короткое сообщение"
        )
        self.assertEqual(feedback.get_short_message(), "Короткое сообщение")


@pytest.mark.django_db
class TestBranchModel:
    @pytest.fixture
    def branch(self):
        return Branch.objects.create(
            name="Главный филиал",
            address="ул. Центральная, 1",
            phone="+79991234567",
            email="main@example.com",
            working_hours="09:00-18:00",
            is_main=True,
            order=1
        )

    def test_name_field(self, branch):
        assert branch._meta.get_field('name').verbose_name == "Название филиала"
        assert branch._meta.get_field('name').max_length == 100
        assert branch.name == "Главный филиал"

    def test_address_field(self, branch):
        assert branch._meta.get_field('address').verbose_name == "Адрес"
        assert branch.address == "ул. Центральная, 1"

    def test_phone_field(self, branch):
        assert branch._meta.get_field('phone').verbose_name == "Телефон"
        assert branch._meta.get_field('phone').max_length == 20

    def test_working_hours_field(self, branch):
        assert branch._meta.get_field('working_hours').verbose_name == "Режим работы"
        assert branch.working_hours == "09:00-18:00"

    def test_map_embed_code_field(self, branch):
        assert branch._meta.get_field('map_embed_code').verbose_name == "Код карты"
        assert branch._meta.get_field('map_embed_code').blank is True

    def test_photo_field(self, branch):
        field = branch._meta.get_field('photo')
        assert field.verbose_name == "Фото"
        assert field.upload_to == "branches/"
        assert field.null is True
        assert field.blank is True

    def test_is_main_field(self, branch):
        assert branch._meta.get_field('is_main').verbose_name == "Главный филиал"
        assert branch._meta.get_field('is_main').default is False
        assert branch.is_main is True

    def test_order_field(self, branch):
        assert branch._meta.get_field('order').verbose_name == "Порядок отображения"
        assert branch._meta.get_field('order').default == 0
        assert branch.order == 1

    def test_meta_options(self, branch):
        assert branch._meta.verbose_name == "Филиал"
        assert branch._meta.verbose_name_plural == "Филиалы"
        assert branch._meta.ordering == ["order"]

    def test_str_method(self, branch):
        assert str(branch) == "Главный филиал"

    def test_get_map_iframe_method(self):
        branch = Branch.objects.create(
            name="Тест",
            address="ул. Тестовая",
            phone="+79991234567",
            email="test@example.com",
            working_hours="09:00-18:00",
            map_embed_code='<iframe width="600" height="400"></iframe>'
        )
        assert 'width="100%"' in branch.get_map_iframe()
        assert 'height="400"' in branch.get_map_iframe()

    def test_photo_upload(self):
        photo = SimpleUploadedFile(
            "test.jpg",
            b"file_content",
            content_type="image/jpeg"
        )
        branch = Branch.objects.create(
            name="Тест с фото",
            address="ул. Тестовая",
            phone="+79991234567",
            email="test@example.com",
            working_hours="09:00-18:00",
            photo=photo
        )
        assert branch.photo.name.startswith("branches/test.jpg")