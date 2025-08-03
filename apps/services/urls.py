from django.urls import path

from . import views

app_name = "services"

urlpatterns = [
    path("", views.ServiceHomeView.as_view(), name="home"),
    path("services/", views.AllServicesView.as_view(), name="all_services"),
    path("services/category/", views.ServiceCategoryListView.as_view(), name="list"),
    path("services/category/<slug:slug>/", views.ServiceCategoryListView.as_view(), name="list_by_category"),
    path("services/<slug:slug>/", views.ServiceDetailView.as_view(), name="detail"),
]
