from .serializer import ShippingAddressSerializer
from .models import ShippingAddress
from rest_framework.generics import ListCreateAPIView
from rest_framework.permissions import IsAuthenticated
# Create your views here.


class ShippingAddressView(ListCreateAPIView):
    queryset = ShippingAddress.objects.all()
    serializer_class = ShippingAddressSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)
