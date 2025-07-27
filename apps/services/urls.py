from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views
from .views import (
    ServiceViewSet,
    ServiceCategoryViewSet,
    PopularServicesAPIView
)


app_name = 'services'


# Для API
router = DefaultRouter()
router.register(r'services', ServiceViewSet, basename='service')
router.register(r'categories', ServiceCategoryViewSet, basename='category')

api_urlpatterns = [
    path('api/', include(router.urls)),
    path('api/popular/', PopularServicesAPIView.as_view(), name='popular-services-api'),
]


urlpatterns = [
    path('', views.ServiceListView.as_view(), name='list'),
    path('category/<slug:category_slug>/',
         views.ServiceListView.as_view(),
         name='category'),
    path('<slug:slug>/', views.ServiceDetailView.as_view(), name='detail'),
]

urlpatterns += api_urlpatterns
