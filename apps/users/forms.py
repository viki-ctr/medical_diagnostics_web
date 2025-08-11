from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm, UserChangeForm
from django.core.exceptions import ValidationError

from .models import DoctorProfile, PatientProfile

User = get_user_model()


class RegisterForm(forms.ModelForm):
    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={"class": "form-control"}),
        help_text="Пароль должен содержать минимум 8 символов",
        label="Пароль"
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={"class": "form-control"}),
        label="Подтверждение пароля"
    )

    class Meta:
        model = User
        fields = ["username", "email", "first_name", "last_name"]
        widgets = {
            "username": forms.TextInput(attrs={"class": "form-control"}),
            "email": forms.EmailInput(attrs={"class": "form-control"}),
            "first_name": forms.TextInput(attrs={"class": "form-control"}),
            "last_name": forms.TextInput(attrs={"class": "form-control"}),
        }

    def clean_password2(self):
        cd = self.cleaned_data
        if cd["password1"] != cd["password2"]:
            raise ValidationError("Пароли не совпадают.")
        if len(cd["password1"]) < 8:
            raise ValidationError("Пароль должен содержать минимум 8 символов.")
        return cd["password2"]

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class LoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={"class": "form-control", "autofocus": True}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={"class": "form-control"}))


class ChangePasswordForm(PasswordChangeForm):
    old_password = forms.CharField(widget=forms.PasswordInput(attrs={"class": "form-control"}), label="Текущий пароль")
    new_password1 = forms.CharField(widget=forms.PasswordInput(attrs={"class": "form-control"}), label="Новый пароль")
    new_password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={"class": "form-control"}), label="Подтверждение пароля"
    )


class PatientProfileForm(forms.ModelForm):
    class Meta:
        model = PatientProfile
        fields = ["birth_date", "gender", "address", "phone", "medical_history"]
        widgets = {
            "birth_date": forms.DateInput(attrs={"class": "form-control", "type": "date"}),
            "gender": forms.Select(attrs={"class": "form-control"}),
            "address": forms.TextInput(attrs={"class": "form-control"}),
            "phone": forms.TextInput(attrs={"class": "form-control"}),
            "medical_history": forms.Textarea(attrs={"class": "form-control", "rows": 3}),
        }


class DoctorProfileForm(forms.ModelForm):
    class Meta:
        model = DoctorProfile
        fields = ["specialty", "department"]
        widgets = {
            "specialty": forms.TextInput(attrs={"class": "form-control"}),
            "department": forms.TextInput(attrs={"class": "form-control"}),
        }


class ProfileUpdateForm(UserChangeForm):
    class Meta:
        model = User
        fields = ["username", "email", "first_name", "last_name"]
