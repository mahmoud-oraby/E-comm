from rest_framework import generics
from .serializer import OrderSerializers
from .models import Order
# Create your views here.


class OrderListCreateView(generics.ListCreateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializers
    pagination_class = None
