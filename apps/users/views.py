from django.contrib import messages
from django.contrib.auth import get_user_model, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView as DjangoLoginView
from django.contrib.auth.views import PasswordChangeView
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import FormView, TemplateView, UpdateView

from .forms import (ChangePasswordForm, DoctorProfileForm, LoginForm, PatientProfileForm, ProfileUpdateForm,
                    RegisterForm)
from .models import DoctorProfile, PatientProfile

User = get_user_model()


class RegisterView(FormView):
    template_name = "users/register.html"
    form_class = RegisterForm
    success_url = reverse_lazy("users:profile")

    def form_valid(self, form):
        user = form.save(commit=False)
        user.set_password(form.cleaned_data["password2"])
        user.save()

        if hasattr(User, "patient_profile"):
            PatientProfile.objects.create(user=user)
        elif hasattr(User, "doctor_profile"):
            DoctorProfile.objects.create(user=user)

        login(self.request, user)
        return super().form_valid(form)


class LoginView(DjangoLoginView):
    template_name = "users/login.html"
    form_class = LoginForm
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy("users:profile")


class LogoutView(LoginRequiredMixin, View):  # Изменяем с TemplateView на View
    def post(self, request, *args, **kwargs):
        logout(request)
        return HttpResponseRedirect(reverse_lazy("users:login"))  # Или возвращаем JSON для API

    def get(self, request, *args, **kwargs):
        logout(request)
        return render(request, "users/logout.html")


class ProfileView(LoginRequiredMixin, TemplateView):
    template_name = "users/profile/profile.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        context["user"] = user

        if hasattr(user, "patient_profile"):
            context["profile"] = user.patient_profile
        elif hasattr(user, "doctor_profile"):
            context["profile"] = user.doctor_profile

        return context


class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    form_class = ProfileUpdateForm
    template_name = "users/profile/profile.html"
    success_url = reverse_lazy("users:profile")

    def get_object(self, queryset=None):
        return self.request.user

    def form_valid(self, form):
        messages.success(self.request, "Профиль успешно обновлен")
        return super().form_valid(form)


class ChangePasswordView(PasswordChangeView):
    template_name = "users/password/change_password.html"
    form_class = ChangePasswordForm
    success_url = "/users/password/change-password-done/"

    def form_valid(self, form):
        user = self.request.user
        user.set_password(form.cleaned_data["new_password1"])
        user.save()
        login(self.request, user)
        return super().form_valid(form)


class PatientProfileView(LoginRequiredMixin, UpdateView):
    template_name = "users/profile/patient_profile.html"
    form_class = PatientProfileForm
    success_url = reverse_lazy("users:profile")

    def get_object(self, queryset=None):
        return self.request.user.patient_profile


class DoctorProfileView(LoginRequiredMixin, UpdateView):
    template_name = "users/profile/doctor_profile.html"
    form_class = DoctorProfileForm
    success_url = reverse_lazy("users:profile")

    def get_object(self, queryset=None):
        return self.request.user.doctor_profile
