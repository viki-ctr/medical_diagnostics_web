from django.shortcuts import get_object_or_404
from django.views.generic import DetailView, ListView, TemplateView

from .models import FAQ, AboutPage, Department, FAQCategory, HomePageContent, SiteSetting, TeamMember, Testimonial


class HomeView(TemplateView):
    template_name = "core/index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(
            {
                "home_content": HomePageContent.objects.filter(is_active=True).first(),
                "testimonials": Testimonial.objects.filter(is_featured=True)[:5],
                "site_settings": SiteSetting.objects.first(),
            }
        )
        return context


class AboutView(TemplateView):
    template_name = "core/about.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(
            {
                "about_page": AboutPage.objects.first(),
                "team_members": TeamMember.objects.filter(is_visible=True).order_by("order"),
                "departments": Department.objects.all(),
            }
        )
        return context


class FAQListView(ListView):
    model = FAQ
    template_name = "core/faq_list.html"
    context_object_name = "faqs"

    def get_queryset(self):
        return FAQ.objects.filter(is_active=True).order_by("category__order", "order")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["categories"] = FAQCategory.objects.all().order_by("order")
        return context


class FAQCategoryView(DetailView):
    model = FAQCategory
    template_name = "core/faq_category.html"
    context_object_name = "category"
    slug_field = "slug"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["faqs"] = FAQ.objects.filter(category=self.object, is_active=True).order_by("order")
        return context


class TeamListView(ListView):
    model = TeamMember
    template_name = "core/team_list.html"
    context_object_name = "team_members"

    def get_queryset(self):
        return TeamMember.objects.filter(is_visible=True).order_by("order")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["departments"] = Department.objects.all()
        return context


class TestimonialListView(ListView):
    model = Testimonial
    template_name = "core/testimonial_list.html"
    context_object_name = "testimonials"
    paginate_by = 10

    def get_queryset(self):
        return Testimonial.objects.all().order_by("-created_at")


class DepartmentDetailView(DetailView):
    model = Department
    template_name = "core/department_detail.html"
    context_object_name = "department"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["team_members"] = TeamMember.objects.filter(department=self.object, is_visible=True).order_by("order")
        return context
