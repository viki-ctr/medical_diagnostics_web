from django.contrib import admin
from .models import Appointment, DoctorSchedule
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
        'custom_actions'
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
    readonly_fields = ('created_at',) if hasattr(Appointment, 'created_at') else ()

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
            'fields': ('notes', 'results', *(['created_at'] if hasattr(Appointment, 'created_at') else [])),
            'classes': ('collapse',)
        })
    )

    def patient_info(self, obj):
        if obj.patient:
            url = reverse("admin:users_user_change", args=[obj.patient.id])
            return format_html('<a href="{}">{}</a>', url, obj.patient.username)
        return "-"

    patient_info.short_description = 'Patient'

    def doctor_info(self, obj):
        if obj.doctor and obj.doctor.user:
            return f"{obj.doctor.user.get_full_name()} ({obj.doctor.specialty})"
        return "-"

    doctor_info.short_description = 'Doctor'

    def service_info(self, obj):
        if obj.service:
            return f"{obj.service.name} ({obj.service.price} руб.)"
        return "-"

    service_info.short_description = 'Service'

    def custom_actions(self, obj):
        change_url = reverse('admin:appointments_appointment_change', args=[obj.id])
        return format_html(
            '<a class="button" href="{}">View</a>&nbsp;'
            '<a class="button" href="{}">Change</a>',
            change_url,
            change_url
        )

    custom_actions.short_description = 'Actions'

    @admin.action(description='Mark selected as confirmed')
    def mark_as_confirmed(self, request, queryset):
        queryset.update(status='confirmed')

    @admin.action(description='Mark selected as completed')
    def mark_as_completed(self, request, queryset):
        queryset.update(status='completed')

    @admin.action(description='Mark selected as cancelled')
    def mark_as_cancelled(self, request, queryset):
        queryset.update(status='cancelled')


@admin.register(DoctorSchedule)
class DoctorScheduleAdmin(admin.ModelAdmin):
    list_display = ('doctor', 'formatted_working_days')

    def formatted_working_days(self, obj):
        days = {0: 'Пн', 1: 'Вт', 2: 'Ср', 3: 'Чт', 4: 'Пт', 5: 'Сб', 6: 'Вс'}
        return ', '.join(days[day] for day in obj.working_days)

    formatted_working_days.short_description = 'Рабочие дни'
