from django.contrib import admin
from .models import ServiceCategory, Service


@admin.register(ServiceCategory)
class ServiceCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'get_service_count')
    search_fields = ('name', 'description')
    prepopulated_fields = {'slug': ('name',)}

    def get_service_count(self, obj):
        return obj.service_set.count()

    get_service_count.short_description = 'Services count'


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'price', 'duration', 'is_available')
    list_filter = ('category', 'is_available')
    search_fields = ('name', 'description', 'preparation')
    list_editable = ('is_available', 'price')
    prepopulated_fields = {'slug': ('name',)}
    filter_horizontal = ()
    fieldsets = (
        (None, {
            'fields': ('category', 'name', 'slug', 'is_available')
        }),
        ('Details', {
            'fields': ('description', 'preparation', 'price', 'duration')
        }),
        ('Additional', {
            'fields': ('image',),
            'classes': ('collapse',)
        })
    )

    class Media:
        js = ('js/admin/service_admin.js',)
        css = {
            'all': ('css/admin/service_admin.css',)
        }
