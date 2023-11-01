from rest_framework import generics, status
from .models import Cart, CartItem
from .serializers import CartSerializer, CartItemSerializer, ListCartItemSerializer
from rest_framework.views import APIView
from rest_framework.response import Response


class CartList(generics.ListCreateAPIView):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer

    def get_object(self):
        return self.queryset.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


# class CartItemCreateView(generics.CreateAPIView):
#     queryset = CartItem.objects.all()
#     create_serializer_class = CartItemSerializer
#     list_serializer_class = ListCartItemSerializer

#     def get_object(self):
#         cart_id = Cart.objects.get(user=self.request.user)
#         print(cart_id)
#         print(self.queryset.filter(cart_id=cart_id))
#         return self.queryset.filter(cart_id=cart_id).order_by("-id")

#     def perform_create(self, serializer):
#         cart_id = Cart.objects.get(user=self.request.user)
#         serializer.save(cart=cart_id)


class CartItemListCreateAPIView(APIView):

    def get(self, request, format=None):
        queryset = CartItem.objects.all()
        serializer = ListCartItemSerializer(
            queryset, many=True, context={"request": request})
        return Response(serializer.data)

    def post(self, request, format=None):

        serializer = CartItemSerializer(
            data=request.data, context={"request": request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
