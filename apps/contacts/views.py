from django.shortcuts import redirect, render
from django.views.generic import TemplateView, ListView
from rest_framework import generics, permissions, viewsets

from .forms import FeedbackForm
from .models import ContactInfo, Feedback, Branch
from .serializers import (
    ContactInfoSerializer,
    FeedbackSerializer,
    BranchSerializer
)


class ContactInfoView(TemplateView):
    template_name = 'contacts/contact_info.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['contact_info'] = ContactInfo.objects.first()
        return context


class BranchesListView(ListView):
    model = Branch
    template_name = 'contacts/branches_list.html'
    context_object_name = 'branches'


def feedback_view(request):
    if request.method == 'POST':
        form = FeedbackForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('contacts:feedback_thanks')
    else:
        form = FeedbackForm()

    return render(request, 'contacts/feedback_form.html', {'form': form})


class FeedbackThanksView(TemplateView):
    template_name = 'contacts/feedback_thanks.html'


class ContactInfoAPIView(generics.RetrieveAPIView):
    """
    Получение контактной информации
    GET /api/contacts/contact-info/
    """
    queryset = ContactInfo.objects.all()
    serializer_class = ContactInfoSerializer
    permission_classes = [permissions.AllowAny]

    def get_object(self):
        return ContactInfo.objects.first()


class FeedbackViewSet(viewsets.ModelViewSet):
    """
    Управление отзывами
    GET, POST /api/contacts/feedback/
    GET, PUT, DELETE /api/contacts/feedback/<id>/
    """
    queryset = Feedback.objects.all()
    serializer_class = FeedbackSerializer

    def get_permissions(self):
        if self.request.method in ['GET', 'POST']:
            return [permissions.AllowAny()]
        return [permissions.IsAdminUser()]

    def perform_create(self, serializer):
        if self.request.user.is_authenticated:
            serializer.save(user=self.request.user)
        else:
            serializer.save()


class BranchViewSet(viewsets.ModelViewSet):
    """
    Управление филиалами клиники
    GET /api/contacts/branches/
    POST, PUT, DELETE /api/contacts/branches/<id>/ (только админ)
    """
    queryset = Branch.objects.all()
    serializer_class = BranchSerializer

    def get_permissions(self):
        if self.request.method == 'GET':
            return [permissions.AllowAny()]
        return [permissions.IsAdminUser()]
