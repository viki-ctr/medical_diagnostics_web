from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    ContactInfoAPIView,
    FeedbackViewSet,
    BranchViewSet, BranchesListView, feedback_view, FeedbackThanksView, ContactInfoView
)


app_name = 'contacts'


router = DefaultRouter()
router.register(r'feedback', FeedbackViewSet, basename='feedback')
router.register(r'branches', BranchViewSet, basename='branches')

urlpatterns = [
    path('', ContactInfoView.as_view(), name='contact-info'),
    path('branches/', BranchesListView.as_view(), name='branches-list'),
    path('feedback/', feedback_view, name='feedback-form'),
    path('feedback/thanks/', FeedbackThanksView.as_view(), name='feedback-thanks'),

    path('api/contact-info/', ContactInfoAPIView.as_view(), name='api-contact-info'),
    path('api/', include(router.urls)),
    ]
