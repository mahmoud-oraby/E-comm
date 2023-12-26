from rest_framework import generics
from .serializer import OrderCreateSerializers, OrderGetSerializer
from .models import Order
# Create your views here.


class OrderCreateView(generics.CreateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderCreateSerializers
    pagination_class = None


class OrderListView(generics.ListAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderGetSerializer
    pagination_class = None
