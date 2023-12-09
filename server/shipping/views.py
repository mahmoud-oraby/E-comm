from .serializer import ShippingAddressCreateSerializer, ShippingAddressListSerializer
from .models import ShippingAddress
from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
# Create your views here.


class ShippingAddressView(ModelViewSet):
    queryset = ShippingAddress.objects.all()
    serializer_class = ShippingAddressCreateSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = None

    def get_serializer_class(self):
        if self.action == "list":
            return ShippingAddressListSerializer
        return ShippingAddressCreateSerializer

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)


class SetDefaultAddress(APIView):
    def post(self, request, id):
        user = request.user
        try:
            shipping_address = ShippingAddress.objects.get(
                user=user, default_address=True)
            shipping_address.default_address = False
            shipping_address.save()
            address = ShippingAddress.objects.get(id=id)
            address.default_address = True
            address.save()
            data = {'message': 'success'}
        except ShippingAddress.DoesNotExist:
            try:
                shipping_address = ShippingAddress.objects.get(id=id)
                shipping_address.default_address = True
                shipping_address.save()
                data = {'message': 'success'}
            except:
                data = {"error": "Not found"}
        return Response(data)
