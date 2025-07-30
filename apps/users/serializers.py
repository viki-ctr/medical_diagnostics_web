from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from django.core import exceptions
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from .models import DoctorProfile, PatientProfile

User = get_user_model()


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, style={"input_type": "password"})
    password2 = serializers.CharField(write_only=True, required=True, style={"input_type": "password"})

    class Meta:
        model = User
        fields = [
            "username",
            "email",
            "password",
            "password2",
            "first_name",
            "last_name",
            "phone",
            "is_patient",
            "is_doctor",
        ]
        extra_kwargs = {"is_patient": {"required": False}, "is_doctor": {"required": False}}

    def validate(self, attrs):
        if attrs["password"] != attrs["password2"]:
            raise serializers.ValidationError({"password": "Пароли не совпадают"})

        try:
            validate_password(attrs["password"])
        except exceptions.ValidationError as e:
            raise serializers.ValidationError({"password": list(e.messages)})

        return attrs

    def create(self, validated_data):
        validated_data.pop("password2")
        user_type = None

        if validated_data.get("is_doctor", False):
            user_type = "is_doctor"
        elif validated_data.get("is_patient", False):
            user_type = "is_patient"

        if not user_type:
            raise serializers.ValidationError({"user_type": "Необходимо указать тип пользователя (пациент или врач)"})

        user = User.objects.create_user(**validated_data)

        # Создаем соответствующий профиль
        if user_type == "is_patient":
            PatientProfile.objects.create(user=user)
        elif user_type == "is_doctor":
            DoctorProfile.objects.create(user=user)

        return user


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True, write_only=True, style={"input_type": "password"})
    new_password = serializers.CharField(required=True, write_only=True, style={"input_type": "password"})
    new_password2 = serializers.CharField(required=True, write_only=True, style={"input_type": "password"})

    def validate(self, attrs):
        if attrs["new_password"] != attrs["new_password2"]:
            raise serializers.ValidationError({"new_password": "Пароли не совпадают"})

        try:
            validate_password(attrs["new_password"])
        except exceptions.ValidationError as e:
            raise serializers.ValidationError({"new_password": list(e.messages)})

        return attrs


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)

        data.update(
            {
                "id": self.user.id,
                "username": self.user.username,
                "email": self.user.email,
                "is_patient": self.user.is_patient,
                "is_doctor": self.user.is_doctor,
            }
        )

        return data


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "email", "first_name", "last_name", "phone", "is_patient", "is_doctor"]
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user


class PatientProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    full_name = serializers.SerializerMethodField()

    class Meta:
        model = PatientProfile
        fields = ["id", "user", "full_name", "birth_date", "address", "medical_history"]

    def get_full_name(self, obj):
        return obj.user.get_full_name()


class DoctorProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    full_name = serializers.SerializerMethodField()
    photo_url = serializers.SerializerMethodField()

    class Meta:
        model = DoctorProfile
        fields = ["id", "user", "full_name", "specialty", "bio", "education", "experience", "photo_url"]

    def get_full_name(self, obj):
        return obj.user.get_full_name()

    def get_photo_url(self, obj):
        if obj.photo:
            return obj.photo.url
        return None
