from django.contrib.auth import get_user_model
from django.contrib.auth.views import LogoutView as DjangoLogoutView
from django.views.generic import TemplateView
from rest_framework import generics, mixins, permissions, status, viewsets
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView

from .models import DoctorProfile, PatientProfile
from .serializers import (ChangePasswordSerializer, CustomTokenObtainPairSerializer, DoctorProfileSerializer,
                          PatientProfileSerializer, RegisterSerializer, UserSerializer)

User = get_user_model()


class RegisterAPIView(generics.CreateAPIView):
    """
    Регистрация нового пользователя+
    POST /api/users/register/
    """

    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]


class CustomTokenObtainPairView(TokenObtainPairView):
    """
    Получение JWT токена (вход)
    POST /api/users/login/
    """

    serializer_class = CustomTokenObtainPairSerializer

    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        if response.status_code == 200:
            user = User.objects.get(username=request.data["username"])
            response.data["user"] = UserSerializer(user).data
        return response


class CurrentUserAPIView(generics.RetrieveAPIView):
    """
    Получение данных текущего пользователя
    GET /api/users/me/
    """

    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user


class ChangePasswordAPIView(generics.UpdateAPIView):
    """
    Смена пароля
    PUT /api/users/change-password/
    """

    serializer_class = ChangePasswordSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user

    def update(self, request, *args, **kwargs):
        user = self.get_object()
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            if not user.check_password(serializer.data.get("old_password")):
                return Response({"old_password": ["Неверный текущий пароль"]}, status=status.HTTP_400_BAD_REQUEST)
            user.set_password(serializer.data.get("new_password"))
            user.save()
            return Response({"status": "Пароль успешно изменен"})

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserViewSet(generics.ListAPIView):
    """
    Список пользователей (только для администраторов)
    GET /api/users/
    """

    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAdminUser]


class PatientProfileViewSet(mixins.RetrieveModelMixin, mixins.UpdateModelMixin, viewsets.GenericViewSet):
    """
    Профиль пациента
    GET, PUT /api/users/patients/<id>/
    """

    queryset = PatientProfile.objects.all()
    serializer_class = PatientProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_permissions(self):
        if self.request.method == "PUT":
            return [permissions.IsAuthenticated(), permissions.IsAdminUser()]
        return [permissions.IsAuthenticated()]


class DoctorProfileViewSet(mixins.RetrieveModelMixin, mixins.UpdateModelMixin, viewsets.GenericViewSet):
    """
    Профиль врача
    GET, PUT /api/users/doctors/<id>/
    """

    queryset = DoctorProfile.objects.all()
    serializer_class = DoctorProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def __str__(self):
        return f"{self.user.username} profile"

    def get_permissions(self):
        if self.request.method == "PUT":
            return [permissions.IsAuthenticated(), permissions.IsAdminUser()]
        return [permissions.IsAuthenticated()]


class LogoutAPIView(APIView):
    def post(self, request):
        try:
            refresh_token = request.data.get("refresh_token")
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response(status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class LoginView(TemplateView):
    template_name = "users/login.html"


class RegisterView(TemplateView):
    template_name = "users/register.html"


class ProfileView(TemplateView):
    template_name = "users/profile.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user'] = self.request.user
        return context


class ChangePasswordView(TemplateView):
    template_name = "users/change_password.html"


class LogoutView(DjangoLogoutView):
    next_page = "home"


class PatientProfileView(TemplateView):
    template_name = "users/patient_profile.html"


class DoctorProfileView(TemplateView):
    template_name = "users/doctor_profile.html"
