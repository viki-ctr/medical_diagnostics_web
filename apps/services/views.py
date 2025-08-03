from django.db.models import Count
from django.shortcuts import get_object_or_404
from django.views.generic import DetailView, ListView, TemplateView

from .models import Service, ServiceCategory


class ServiceHomeView(TemplateView):
    template_name = "services/home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(
            {
                "popular_services": Service.objects.filter(is_available=True)
                .annotate(appointments_count=Count("appointments"))
                .order_by("-appointments_count")[:6],
                "categories": ServiceCategory.objects.annotate(service_count=Count("services")).filter(
                    service_count__gt=0
                ),
                "all_services": Service.objects.filter(is_available=True)[:10],
            }
        )
        return context


class ServiceCategoryListView(ListView):
    model = Service
    template_name = "services/list.html"
    context_object_name = "services"
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset().filter(is_available=True)
        slug = self.kwargs.get("slug")
        if slug:
            self.category = get_object_or_404(ServiceCategory, slug=slug)
            queryset = queryset.filter(category=self.category)
        return queryset.select_related("category")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if hasattr(self, "category"):
            context["category"] = self.category
        context["categories"] = ServiceCategory.objects.annotate(service_count=Count("services")).filter(
            service_count__gt=0
        )
        return context


class ServiceDetailView(DetailView):
    model = Service
    template_name = "services/detail.html"
    context_object_name = "service"
    slug_url_kwarg = "slug"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["related_services"] = Service.objects.filter(category=self.object.category, is_available=True).exclude(
            id=self.object.id
        )[:4]
        return context


class AllServicesView(ListView):
    model = Service
    template_name = "services/all_services.html"
    context_object_name = "services"
    paginate_by = 12

    def get_queryset(self):
        return Service.objects.filter(is_available=True).select_related("category")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["categories"] = ServiceCategory.objects.annotate(service_count=Count("services")).filter(
            service_count__gt=0
        )
        return context
