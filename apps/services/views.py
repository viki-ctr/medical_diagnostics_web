from django.views.generic import ListView, DetailView
from .models import Service, ServiceCategory


class ServiceListView(ListView):
    model = Service
    template_name = 'services/list.html'
    context_object_name = 'services'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = ServiceCategory.objects.all()
        return context


class ServiceDetailView(DetailView):
    model = Service
    template_name = 'services/detail.html'
    context_object_name = 'service'
