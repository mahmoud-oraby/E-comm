from rest_framework import viewsets, permissions
from .serializers import *
from .models import Message
# Create your views here.


class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    pagination_class = None

    def get_queryset(self):
        queryset = Message.objects.all()
        if not self.request.user.is_superuser:
            queryset = queryset.none()
        return queryset
