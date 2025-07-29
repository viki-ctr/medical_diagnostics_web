from django.views.generic import TemplateView, DetailView, ListView
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from .models import (
    HomePageContent,
    AboutPage,
    FAQ,
    FAQCategory,
    TeamMember,
    Testimonial,
    SiteSetting
)
from .serializers import (
    HomePageContentSerializer,
    AboutPageSerializer,
    FAQSerializer,
    FAQCategorySerializer,
    TeamMemberSerializer,
    TestimonialSerializer,
    SiteSettingSerializer
)


class HomeView(TemplateView):
    template_name = 'core/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['home_content'] = HomePageContent.objects.filter(is_active=True).first()
        context['testimonials'] = Testimonial.objects.filter(is_featured=True)[:5]
        return context


class AboutView(TemplateView):
    template_name = 'core/about.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['about_page'] = AboutPage.objects.first()
        context['team_members'] = TeamMember.objects.filter(is_visible=True).order_by('order')
        return context


class FAQListView(ListView):
    model = FAQ
    template_name = 'core/faq_list.html'
    context_object_name = 'faqs'

    def get_queryset(self):
        return FAQ.objects.filter(is_active=True).order_by('category__order', 'order')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = FAQCategory.objects.all().order_by('order')
        return context


class FAQCategoryView(DetailView):
    model = FAQCategory
    template_name = 'core/faq_category.html'
    context_object_name = 'category'
    slug_field = 'slug'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['faqs'] = FAQ.objects.filter(
            category=self.object,
            is_active=True
        ).order_by('order')
        return context


class TeamListView(ListView):
    model = TeamMember
    template_name = 'core/team_list.html'
    context_object_name = 'team_members'

    def get_queryset(self):
        return TeamMember.objects.filter(is_visible=True).order_by('order')


class TestimonialListView(ListView):
    model = Testimonial
    template_name = 'core/testimonial_list.html'
    context_object_name = 'testimonials'
    paginate_by = 10

    def get_queryset(self):
        return Testimonial.objects.all().order_by('-created_at')


class HomePageContentAPIView(generics.RetrieveAPIView):
    """
    API для получения активного контента главной страницы
    GET /api/home-content/
    """
    serializer_class = HomePageContentSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_object(self):
        return HomePageContent.objects.filter(is_active=True).first()

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        if not instance:
            return Response(
                {"detail": "Active home page content not found"},
                status=status.HTTP_404_NOT_FOUND
            )
        serializer = self.get_serializer(instance)
        return Response(serializer.data)


class AboutPageAPIView(generics.RetrieveAPIView):
    """
    API для получения страницы "О клинике"
    GET /api/about-page/
    """
    serializer_class = AboutPageSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_object(self):
        return AboutPage.objects.first()

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        if not instance:
            return Response(
                {"detail": "About page not found"},
                status=status.HTTP_404_NOT_FOUND
            )
        serializer = self.get_serializer(instance)
        return Response(serializer.data)


class FAQCategoryListAPIView(generics.ListAPIView):
    """
    API для получения списка категорий FAQ
    GET /api/faq/categories/
    """
    queryset = FAQCategory.objects.all().order_by('order')
    serializer_class = FAQCategorySerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


class FAQListAPIView(generics.ListAPIView):
    """
    API для получения списка FAQ
    GET /api/faq/
    GET /api/faq/?category=<category_id>
    """
    serializer_class = FAQSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        queryset = FAQ.objects.filter(is_active=True).order_by('order')
        category_id = self.request.query_params.get('category')
        if category_id:
            queryset = queryset.filter(category_id=category_id)
        return queryset


class TeamMemberListAPIView(generics.ListAPIView):
    """
    API для получения списка членов команды
    GET /api/team/
    """
    serializer_class = TeamMemberSerializer
    permission_classes = [permissions.AllowAny]
    queryset = TeamMember.objects.filter(is_visible=True).order_by('order')

    def get_serializer_context(self):
        return {'request': self.request}


class TestimonialListAPIView(generics.ListAPIView):
    """
    API для получения списка отзывов
    GET /api/testimonials/
    GET /api/testimonials/?featured=true
    """
    serializer_class = TestimonialSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        queryset = Testimonial.objects.all().order_by('-created_at')
        featured = self.request.query_params.get('featured')
        if featured and featured.lower() == 'true':
            queryset = queryset.filter(is_featured=True)
        return queryset


class SiteSettingAPIView(generics.RetrieveAPIView):
    """
    API для получения настроек сайта
    GET /api/site-settings/
    """
    serializer_class = SiteSettingSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_object(self):
        return SiteSetting.objects.first()

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        if not instance:
            return Response(
                {"detail": "Site settings not found"},
                status=status.HTTP_404_NOT_FOUND
            )
        serializer = self.get_serializer(instance)
        return Response(serializer.data)


class SiteContentAPIView(APIView):
    """
    Комбинированный API для получения всего контента сайта
    GET /api/site-content/
    """
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request):
        data = {
            'home_content': HomePageContentSerializer(
                HomePageContent.objects.filter(is_active=True).first()
            ).data,
            'about_page': AboutPageSerializer(
                AboutPage.objects.first()
            ).data,
            'site_settings': SiteSettingSerializer(
                SiteSetting.objects.first()
            ).data,
            'featured_testimonials': TestimonialSerializer(
                Testimonial.objects.filter(is_featured=True)[:5],
                many=True
            ).data,
            'team_members': TeamMemberSerializer(
                TeamMember.objects.filter(is_visible=True).order_by('order'),
                many=True
            ).data
        }
        return Response(data)