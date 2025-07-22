from django.contrib import admin
from .models import AboutPage, TeamMember


class TeamMemberInline(admin.TabularInline):
    model = TeamMember
    extra = 1
    fields = ('name', 'position', 'photo', 'is_visible')
    ordering = ('order',)


@admin.register(AboutPage)
class AboutPageAdmin(admin.ModelAdmin):
    list_display = ('title', 'updated_at')
    fields = ('title', 'content', 'mission', 'values')
    inlines = [TeamMemberInline]

    def has_add_permission(self, request):
        return not AboutPage.objects.exists()
