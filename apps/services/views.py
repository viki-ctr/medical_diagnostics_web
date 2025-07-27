from django.db.models import Count
from django.views.generic import ListView, DetailView
from rest_framework import viewsets, generics, permissions
from .models import Service, ServiceCategory
from .serializers import ServiceSerializer, ServiceCategorySerializer


class ServiceListView(ListView):
    model = Service
    template_name = 'services/list.html'
    context_object_name = 'services'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        category_slug = self.kwargs.get('category_slug')
        if category_slug:
            queryset = queryset.filter(category__slug=category_slug)
        return queryset.select_related('category')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = ServiceCategory.objects.annotate(
            service_count=Count('service')
        ).filter(service_count__gt=0)
        return context


class ServiceDetailView(DetailView):
    model = Service
    template_name = 'services/detail.html'
    context_object_name = 'service'
    slug_url_kwarg = 'slug'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['related_services'] = Service.objects.filter(
            category=self.object.category
        ).exclude(id=self.object.id)[:4]
        return context


class ServiceViewSet(viewsets.ModelViewSet):
    queryset = Service.objects.filter(is_available=True)
    serializer_class = ServiceSerializer
    lookup_field = 'slug'


class ServiceCategoryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = ServiceCategory.objects.annotate(
        services_count=Count('services')
    ).filter(services_count__gt=0)
    serializer_class = ServiceCategorySerializer
    permission_classes = [permissions.AllowAny]
    lookup_field = 'slug'


class PopularServicesAPIView(generics.ListAPIView):
    serializer_class = ServiceSerializer

    def get_queryset(self):
        return Service.objects.filter(
            is_available=True
        ).annotate(
            appointments_count=Count('appointments')
        ).order_by('-appointments_count')[:8]
