from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, PatientProfile, DoctorProfile

from django.contrib.auth import get_user_model

User = get_user_model()


class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'is_patient', 'is_doctor', 'is_staff')
    list_filter = ('is_patient', 'is_doctor', 'is_staff', 'is_superuser')
    search_fields = ('username', 'email', 'first_name', 'last_name')
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'email', 'phone')}),
        ('Permissions', {
            'fields': (
            'is_active', 'is_staff', 'is_superuser', 'is_patient', 'is_doctor', 'groups', 'user_permissions'),
        }),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2', 'is_patient', 'is_doctor'),
        }),
    )


@admin.register(PatientProfile)
class PatientProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'birth_date', 'get_phone')
    search_fields = ('user__username', 'user__email', 'user__first_name', 'user__last_name')
    list_select_related = ('user',)
    raw_id_fields = ('user',)

    def get_phone(self, obj):
        return obj.user.phone

    get_phone.short_description = 'Phone'


@admin.register(DoctorProfile)
class DoctorProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'specialty', 'get_email')
    list_filter = ('specialty',)
    search_fields = ('user__username', 'specialty', 'user__email')
    filter_horizontal = ()
    raw_id_fields = ('user',)

    def get_email(self, obj):
        return obj.user.email

    get_email.short_description = 'Email'


admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)
