from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, TemplateView, UpdateView

from .forms import FeedbackForm
from .models import Branch, ContactInfo, Feedback


class ContactInfoView(TemplateView):
    template_name = "contacts/contact_info.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["contact_info"] = ContactInfo.objects.first()
        context["branches"] = Branch.objects.filter(is_main=True).first()  # Главный филиал
        return context


class BranchesListView(ListView):
    model = Branch
    template_name = "contacts/branches_list.html"
    context_object_name = "branches"
    ordering = ["order"]


class FeedbackCreateView(CreateView):
    model = Feedback
    form_class = FeedbackForm
    template_name = "contacts/feedback_form.html"
    success_url = reverse_lazy("contacts:feedback_thanks")


class FeedbackThanksView(TemplateView):
    template_name = "contacts/feedback_thanks.html"


class FeedbackListView(LoginRequiredMixin, ListView):
    model = Feedback
    template_name = "contacts/feedback_list.html"
    context_object_name = "feedbacks"
    paginate_by = 20

    def get_queryset(self):
        return super().get_queryset().filter(is_published=True)


class FeedbackUpdateView(LoginRequiredMixin, UpdateView):
    model = Feedback
    fields = ["is_processed"]
    template_name = "contacts/feedback_update.html"
    success_url = reverse_lazy("contacts:feedback_list")
