from rest_framework import serializers

from .models import FAQ, AboutPage, FAQCategory, HomePageContent, SiteSetting, TeamMember, Testimonial


class TeamMemberSerializer(serializers.ModelSerializer):
    photo_url = serializers.SerializerMethodField()
    department = serializers.StringRelatedField()

    class Meta:
        model = TeamMember
        fields = [
            "id",
            "name",
            "position",
            "photo_url",
            "bio",
            "education",
            "experience",
            "specialization",
            "department",
        ]
        read_only_fields = fields

    def get_photo_url(self, obj):
        request = self.context.get("request")
        if obj.photo_url and request:
            return request.build_absolute_uri(obj.photo_url)
        return None


class AboutPageSerializer(serializers.ModelSerializer):
    team_members = TeamMemberSerializer(many=True, read_only=True)

    class Meta:
        model = AboutPage
        fields = ["id", "title", "content", "mission", "values", "team_members", "updated_at"]


class HomePageContentSerializer(serializers.ModelSerializer):
    featured_image_url = serializers.SerializerMethodField()

    class Meta:
        model = HomePageContent
        fields = [
            "id",
            "main_title",
            "main_description",
            "services_title",
            "testimonials_title",
            "featured_image_url",
            "is_active",
            "updated_at",
        ]

    def get_featured_image_url(self, obj):
        if obj.featured_image:
            return obj.featured_image.url
        return None


class TestimonialSerializer(serializers.ModelSerializer):
    photo_url = serializers.SerializerMethodField()
    author_initials = serializers.SerializerMethodField()

    class Meta:
        model = Testimonial
        fields = [
            "id",
            "author",
            "position",
            "content",
            "photo_url",
            "author_initials",
            "rating",
            "is_featured",
            "created_at",
        ]

    def get_photo_url(self, obj):
        if obj.photo:
            return obj.photo.url
        return None

    def get_author_initials(self, obj):
        parts = obj.author.split()
        if len(parts) >= 2:
            return f"{parts[0][0]}{parts[1][0]}".upper()
        return obj.author[:2].upper()


class FAQSerializer(serializers.ModelSerializer):
    class Meta:
        model = FAQ
        fields = ["id", "question", "answer", "category", "order", "is_active"]


class FAQCategorySerializer(serializers.ModelSerializer):
    faqs = FAQSerializer(many=True, read_only=True)

    class Meta:
        model = FAQCategory
        fields = ["id", "name", "slug", "description", "order", "faqs"]


class SiteSettingSerializer(serializers.ModelSerializer):
    logo_url = serializers.SerializerMethodField()
    favicon_url = serializers.SerializerMethodField()

    class Meta:
        model = SiteSetting
        fields = [
            "site_name",
            "logo_url",
            "favicon_url",
            "phone",
            "email",
            "address",
            "working_hours",
            "facebook_url",
            "instagram_url",
            "telegram_url",
            "meta_description",
            "meta_keywords",
        ]

    def get_logo_url(self, obj):
        if obj.logo:
            return obj.logo.url
        return None

    def get_favicon_url(self, obj):
        if obj.favicon:
            return obj.favicon.url
        return None
