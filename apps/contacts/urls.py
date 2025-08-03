from django.urls import path

from .views import (BranchesListView, ContactInfoView, FeedbackCreateView, FeedbackListView, FeedbackThanksView,
                    FeedbackUpdateView)

app_name = "contacts"


urlpatterns = [
    path("", ContactInfoView.as_view(), name="contact-info"),
    path("branches/", BranchesListView.as_view(), name="branches-list"),
    path("feedback/", FeedbackCreateView.as_view(), name="feedback-form"),
    path("feedback/thanks/", FeedbackThanksView.as_view(), name="feedback-thanks"),
    path("feedback/list/", FeedbackListView.as_view(), name="feedback-list"),
    path("feedback/<int:pk>/update/", FeedbackUpdateView.as_view(), name="feedback-update"),
]
