from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import (
    ContactInfoAPIView,
    FeedbackViewSet,
    BranchViewSet
)

router = DefaultRouter()
router.register(r'feedback', FeedbackViewSet, basename='feedback')
router.register(r'branches', BranchViewSet, basename='branch')

urlpatterns = [
    path('contact-info/',
         ContactInfoAPIView.as_view(),
         name='contact-info'),
] + router.urls
