from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from . import views


app_name = 'users'


urlpatterns = [
    path('api/login/', views.CustomTokenObtainPairView.as_view(), name='api_login'),
    path('api/login/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/register/', views.RegisterAPIView.as_view(), name='api_register'),
    path('api/me/', views.CurrentUserAPIView.as_view(), name='api_current_user'),
    path('api/change-password/', views.ChangePasswordAPIView.as_view(), name='api_change_password'),
    path('api/logout/', views.LogoutAPIView.as_view(), name='api_logout'),


    path('login/', views.LoginView.as_view(), name='login'),
    path('register/', views.RegisterView.as_view(), name='register'),
    path('profile/', views.ProfileView.as_view(), name='profile'),
    path('profile/change-password/', views.ChangePasswordView.as_view(), name='change_password'),
    path('logout/', views.LogoutView.as_view(), name='logout'),


    path('patients/<int:pk>/', views.PatientProfileView.as_view(), name='patient_profile'),
    path('doctors/<int:pk>/', views.DoctorProfileView.as_view(), name='doctor_profile'),
]