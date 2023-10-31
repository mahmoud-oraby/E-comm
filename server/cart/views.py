from rest_framework import generics
from .models import Cart, CartItem
from .serializers import CartSerializer, CartItemSerializer


class CartList(generics.ListCreateAPIView):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer

    def get_object(self):
        return self.queryset.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class CartItemList(generics.ListCreateAPIView):
    queryset = CartItem.objects.all()
    serializer_class = CartItemSerializer

    def get_object(self):
        cart_id = Cart.objects.get(user=self.request.user)
        print(cart_id)
        print(self.queryset.filter(cart_id=cart_id))
        return self.queryset.filter(cart_id=cart_id).order_by("-id")

    def perform_create(self, serializer):
        cart_id = Cart.objects.get(user=self.request.user)
        serializer.save(cart=cart_id)
