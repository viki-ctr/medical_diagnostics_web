from django import forms
from django.contrib import admin
from .models import AboutPage, TeamMember, HomePageContent, Testimonial, FAQ, FAQCategory, SiteSetting


class TeamMemberInline(admin.TabularInline):
    model = TeamMember
    extra = 1
    fields = ('name', 'position', 'photo', 'is_visible')
    ordering = ('order',)


class AboutPageForm(forms.ModelForm):
    class Meta:
        model = AboutPage
        widgets = {
            'content': forms.Textarea(attrs={'rows': 10, 'cols': 100}),
        }
        fields = '__all__'



@admin.register(AboutPage)
class AboutPageAdmin(admin.ModelAdmin):
    list_display = ('title', 'updated_at')
    fields = ('title', 'content', 'mission', 'values')
    inlines = [TeamMemberInline]

    def has_add_permission(self, request):
        return not AboutPage.objects.exists()


@admin.register(HomePageContent)
class HomePageContentAdmin(admin.ModelAdmin):
    list_display = ('main_title', 'is_active', 'updated_at')
    list_editable = ('is_active',)


@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = ('author', 'rating_stars', 'is_featured', 'created_at')
    list_editable = ('is_featured',)
    list_filter = ('rating', 'is_featured')

    def rating_stars(self, obj):
        return obj.stars()

    rating_stars.short_description = 'Рейтинг'


class FAQInline(admin.TabularInline):
    model = FAQ
    extra = 1
    fields = ('question', 'answer', 'order', 'is_active')


@admin.register(FAQCategory)
class FAQCategoryAdmin(admin.ModelAdmin):
    inlines = [FAQInline]
    list_display = ('name', 'slug', 'order')
    prepopulated_fields = {"slug": ("name",)}


@admin.register(SiteSetting)
class SiteSettingAdmin(admin.ModelAdmin):
    def has_add_permission(self, request):
        return not SiteSetting.objects.exists()
