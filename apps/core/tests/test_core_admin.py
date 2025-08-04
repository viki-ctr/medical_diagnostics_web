from django.test import TestCase, RequestFactory
from django.contrib.admin.sites import AdminSite
from django.contrib.auth import get_user_model
from django import forms

from apps.core.admin import (
    AboutPageAdmin, HomePageContentAdmin, TestimonialAdmin,
    FAQCategoryAdmin, SiteSettingAdmin, AboutPageForm, TeamMemberInline, FAQInline
)
from apps.core.models import (
    AboutPage, HomePageContent, Testimonial,
    FAQCategory, SiteSetting, TeamMember, FAQ
)

User = get_user_model()


class MockRequest:
    pass


class MockSuperUser:
    def has_perm(self, perm):
        return True


class CoreAdminTest(TestCase):
    def setUp(self):
        self.site = AdminSite()
        self.factory = RequestFactory()
        self.superuser = User.objects.create_superuser(
            username='admin',
            email='admin@example.com',
            password='password'
        )
        self.request = self.factory.get('/admin/')
        self.request.user = self.superuser


class AboutPageAdminTest(CoreAdminTest):
    def setUp(self):
        super().setUp()
        self.model_admin = AboutPageAdmin(AboutPage, self.site)

    def test_has_add_permission_when_no_objects(self):
        self.assertTrue(self.model_admin.has_add_permission(self.request))

    def test_has_add_permission_when_object_exists(self):
        AboutPage.objects.create(title="Test", content="Test")
        self.assertFalse(self.model_admin.has_add_permission(self.request))

    def test_list_display(self):
        self.assertEqual(self.model_admin.list_display, ("title", "updated_at"))

    def test_fields(self):
        self.assertEqual(self.model_admin.fields, ("title", "content", "mission", "values"))

    def test_inlines(self):
        self.assertEqual(len(self.model_admin.inlines), 1)
        self.assertEqual(self.model_admin.inlines[0].__name__, "TeamMemberInline")


class AboutPageFormTest(TestCase):
    def test_form_meta(self):
        self.assertEqual(AboutPageForm.Meta.model, AboutPage)
        self.assertEqual(AboutPageForm.Meta.fields, "__all__")
        self.assertIsInstance(AboutPageForm.Meta.widgets["content"], forms.Textarea)
        self.assertEqual(AboutPageForm.Meta.widgets["content"].attrs, {"rows": 10, "cols": 100})


class HomePageContentAdminTest(CoreAdminTest):
    def setUp(self):
        super().setUp()
        self.model_admin = HomePageContentAdmin(HomePageContent, self.site)

    def test_list_display(self):
        self.assertEqual(
            self.model_admin.list_display,
            ("main_title", "is_active", "updated_at")
        )

    def test_list_editable(self):
        self.assertEqual(self.model_admin.list_editable, ("is_active",))


class TestimonialAdminTest(CoreAdminTest):
    def setUp(self):
        super().setUp()
        self.model_admin = TestimonialAdmin(Testimonial, self.site)

    def test_list_display(self):
        self.assertEqual(
            self.model_admin.list_display,
            ("author", "rating_stars", "is_featured", "created_at")
        )

    def test_list_editable(self):
        self.assertEqual(self.model_admin.list_editable, ("is_featured",))

    def test_list_filter(self):
        self.assertEqual(
            self.model_admin.list_filter,
            ("rating", "is_featured")
        )

    def test_rating_stars_method(self):
        testimonial = Testimonial.objects.create(
            author="Test",
            content="Test",
            rating=4
        )
        self.assertEqual(self.model_admin.rating_stars(testimonial), "★★★★☆")


class FAQCategoryAdminTest(CoreAdminTest):
    def setUp(self):
        super().setUp()
        self.model_admin = FAQCategoryAdmin(FAQCategory, self.site)

    def test_inlines(self):
        self.assertEqual(len(self.model_admin.inlines), 1)
        self.assertEqual(self.model_admin.inlines[0].__name__, "FAQInline")

    def test_list_display(self):
        self.assertEqual(
            self.model_admin.list_display,
            ("name", "slug", "order")
        )

    def test_prepopulated_fields(self):
        self.assertEqual(
            self.model_admin.prepopulated_fields,
            {"slug": ("name",)}
        )


class SiteSettingAdminTest(CoreAdminTest):
    def setUp(self):
        super().setUp()
        self.model_admin = SiteSettingAdmin(SiteSetting, self.site)

    def test_has_add_permission_when_no_objects(self):
        self.assertTrue(self.model_admin.has_add_permission(self.request))

    def test_has_add_permission_when_object_exists(self):
        SiteSetting.objects.create(site_name="Test")
        self.assertFalse(self.model_admin.has_add_permission(self.request))


class TeamMemberInlineTest(TestCase):
    def test_inline_config(self):
        self.assertEqual(TeamMemberInline.model, TeamMember)
        self.assertEqual(TeamMemberInline.extra, 1)
        self.assertEqual(TeamMemberInline.fields, ("name", "position", "photo", "is_visible"))
        self.assertEqual(TeamMemberInline.ordering, ("order",))


class FAQInlineTest(TestCase):
    def test_inline_config(self):
        self.assertEqual(FAQInline.model, FAQ)
        self.assertEqual(FAQInline.extra, 1)
        self.assertEqual(FAQInline.fields, ("question", "answer", "order", "is_active"))
