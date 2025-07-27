from rest_framework import serializers
from .models import ContactInfo, Feedback

class ContactInfoSerializer(serializers.ModelSerializer):
    map_embed = serializers.CharField(source='map_embed_code', read_only=True)

    class Meta:
        model = ContactInfo
        fields = [
            'address',
            'phone',
            'email',
            'working_hours',
            'map_embed'
        ]

class FeedbackSerializer(serializers.ModelSerializer):
    class Meta:
        model = Feedback
        fields = [
            'id',
            'name',
            'email',
            'phone',
            'subject',
            'message',
            'created_at',
            'is_processed'
        ]
        read_only_fields = ['created_at', 'is_processed']
