from django.urls import path

from .views import (AboutView, DepartmentDetailView, FAQCategoryView, FAQListView, HomeView, TeamListView,
                    TestimonialListView)

app_name = "core"

urlpatterns = [
    path("", HomeView.as_view(), name="home"),
    path("about/", AboutView.as_view(), name="about"),
    path("faq/", FAQListView.as_view(), name="faq_list"),
    path("faq/category/<slug:slug>/", FAQCategoryView.as_view(), name="faq_category"),
    path("team/", TeamListView.as_view(), name="team_list"),
    path("team/department/<int:pk>/", DepartmentDetailView.as_view(), name="department_detail"),
    path("testimonials/", TestimonialListView.as_view(), name="testimonial_list"),
]
