from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html

from .models import ContactInfo, Feedback


@admin.register(ContactInfo)
class ContactInfoAdmin(admin.ModelAdmin):
    list_display = ("address_short", "phone", "email", "working_hours")
    fields = ("address", "phone", "email", "working_hours", "map_embed_code")

    def address_short(self, obj):
        return obj.address[:50] + "..." if len(obj.address) > 50 else obj.address

    address_short.short_description = "Address"

    def has_add_permission(self, request):
        return not ContactInfo.objects.exists()


@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "subject", "created_at", "is_processed", "process_action")
    list_filter = ("is_processed", "created_at")
    search_fields = ("name", "email", "subject", "message")
    readonly_fields = ("created_at",)
    list_editable = ("is_processed",)
    date_hierarchy = "created_at"

    fieldsets = (
        (None, {"fields": ("name", "email", "phone", "subject")}),
        ("Message", {"fields": ("message",), "classes": ("collapse",)}),
        ("Status", {"fields": ("is_processed", "created_at")}),
    )

    def process_action(self, obj):
        return format_html(
            '<a class="button" href="{}">Process</a>', reverse("admin:contacts_feedback_change", args=[obj.id])
        )

    process_action.short_description = "Action"
    process_action.allow_tags = True
