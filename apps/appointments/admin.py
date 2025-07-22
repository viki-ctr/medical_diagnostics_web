from django.contrib import admin
from .models import Appointment
from django.utils.html import format_html
from django.urls import reverse


@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'patient_info',
        'doctor_info',
        'service_info',
        'appointment_date',
        'status',
        'actions'
    )
    list_filter = ('status', 'appointment_date', 'doctor', 'service')
    search_fields = (
        'patient__username',
        'patient__email',
        'doctor__user__username',
        'service__name'
    )
    list_select_related = ('patient', 'doctor', 'service')
    date_hierarchy = 'appointment_date'
    actions = ['mark_as_confirmed', 'mark_as_completed', 'mark_as_cancelled']
    readonly_fields = ('created_at',)

    fieldsets = (
        ('Main', {
            'fields': (
                'patient',
                'doctor',
                'service',
                'appointment_date',
                'status'
            )
        }),
        ('Details', {
            'fields': ('notes', 'results', 'created_at'),
            'classes': ('collapse',)
        })
    )

    def patient_info(self, obj):
        url = reverse("admin:accounts_customuser_change", args=[obj.patient.id])
        return format_html('<a href="{}">{}</a>', url, obj.patient.username)

    patient_info.short_description = 'Patient'

    def doctor_info(self, obj):
        return f"{obj.doctor.user.get_full_name()} ({obj.doctor.specialty})"

    doctor_info.short_description = 'Doctor'

    def service_info(self, obj):
        return f"{obj.service.name} ({obj.service.price} руб.)"

    service_info.short_description = 'Service'

    def actions(self, obj):
        return format_html(
            '<a class="button" href="{}">View</a>&nbsp;'
            '<a class="button" href="{}">Change</a>',
            reverse('admin:appointments_appointment_change', args=[obj.id]),
            reverse('admin:appointments_appointment_change', args=[obj.id])
        )

    actions.short_description = 'Actions'
    actions.allow_tags = True

    @admin.action(description='Mark selected as confirmed')
    def mark_as_confirmed(self, request, queryset):
        queryset.update(status='confirmed')

    @admin.action(description='Mark selected as completed')
    def mark_as_completed(self, request, queryset):
        queryset.update(status='completed')

    @admin.action(description='Mark selected as cancelled')
    def mark_as_cancelled(self, request, queryset):
        queryset.update(status='cancelled')
