from django.contrib import admin
from django.db.models import Count

from .models import Service, ServiceCategory


@admin.register(ServiceCategory)
class ServiceCategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "service_count")
    search_fields = ("name", "description")
    prepopulated_fields = {"slug": ("name",)}

    def get_queryset(self, request):
        return super().get_queryset(request).annotate(
            service_count=Count('services')
        )

    def service_count(self, obj):
        return obj.service_count

    service_count.admin_order_field = 'service_count'


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ("name", "category", "price", "duration", "is_available")
    list_filter = ("category", "is_available")
    search_fields = ("name", "description", "preparation")
    list_editable = ("is_available", "price")
    prepopulated_fields = {"slug": ("name",)}
    filter_horizontal = ()
    fieldsets = (
        (None, {"fields": ("category", "name", "slug", "is_available")}),
        ("Детали", {"fields": ("description", "preparation", "price", "duration")}),
        ("Дополнительно", {"fields": ("image",), "classes": ("collapse",)}),
    )

    class Media:
        js = ("js/admin/service_admin.js",)
        css = {"all": ("css/admin/service_admin.css",)}
