from rest_framework import generics, permissions, viewsets
from .models import ContactInfo, Feedback, Branch
from .serializers import (
    ContactInfoSerializer,
    FeedbackSerializer,
    BranchSerializer
)


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
        if self.request.method == 'POST':
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
