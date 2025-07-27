from django.urls import path
from . import views
from .views import (
    HomePageContentAPIView,
    AboutPageAPIView,
    FAQCategoryListAPIView,
    FAQListAPIView,
    TeamMemberListAPIView,
    TestimonialListAPIView,
    SiteSettingAPIView,
    SiteContentAPIView
)


app_name = 'core'


urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('about/', views.AboutView.as_view(), name='about'),
    path('faq/', views.FAQListView.as_view(), name='faq_list'),
    path('faq/category/<slug:slug>/', views.FAQCategoryView.as_view(), name='faq_category'),

    path('home-content/', HomePageContentAPIView.as_view(), name='home-content'),
    path('about-page/', AboutPageAPIView.as_view(), name='about-page'),
    path('faq/categories/', FAQCategoryListAPIView.as_view(), name='faq-categories'),
    path('faq/', FAQListAPIView.as_view(), name='faq-list'),
    path('team/', TeamMemberListAPIView.as_view(), name='team-list'),
    path('testimonials/', TestimonialListAPIView.as_view(), name='testimonial-list'),
    path('site-settings/', SiteSettingAPIView.as_view(), name='site-settings'),
    path('site-content/', SiteContentAPIView.as_view(), name='site-content'),
]
