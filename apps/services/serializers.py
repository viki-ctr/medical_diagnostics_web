from rest_framework import serializers
from .models import Service, ServiceCategory


class ServiceCategorySerializer(serializers.ModelSerializer):
    service_count = serializers.SerializerMethodField()

    class Meta:
        model = ServiceCategory
        fields = [
            'id',
            'name',
            'slug',
            'description',
            'service_count'
        ]

    def get_service_count(self, obj):
        return obj.service_set.count()


class ServiceSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source='category.name', read_only=True)
    image_url = serializers.SerializerMethodField()
    duration_formatted = serializers.SerializerMethodField()

    class Meta:
        model = Service
        fields = [
            'id',
            'name',
            'category',
            'category_name',
            'description',
            'short_description',
            'price',
            'duration',
            'duration_formatted',
            'preparation',
            'image_url',
            'is_available',
            'slug'
        ]
        extra_kwargs = {
            'slug': {'read_only': True}
        }

    def get_image_url(self, obj):
        if obj.image:
            return obj.image.url
        return None

    def get_duration_formatted(self, obj):
        total_seconds = obj.duration.total_seconds()
        hours = int(total_seconds // 3600)
        minutes = int((total_seconds % 3600) // 60)
        return f"{hours} ч {minutes} мин" if hours else f"{minutes} мин"
