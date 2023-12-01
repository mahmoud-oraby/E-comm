from rest_framework import generics, status
from .models import Cart, CartItem
from .serializers import CartSerializer, CartItemSerializer, ListCartItemSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from coupon.serializers import CouponSerializer
from django.db.models import Sum


class CartList(generics.ListAPIView):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = None

    def get_queryset(self):
        return Cart.objects.filter(user=self.request.user)


class CartItemListCreateAPIView(APIView):

    def get(self, request, format=None):
        queryset = CartItem.objects.filter(cart_id__user_id=self.request.user)
        cart = Cart.objects.get(user=request.user)
        serializer = ListCartItemSerializer(
            queryset, many=True, context={"request": request})
        coupon_serializer = CouponSerializer(cart.coupon)

        return Response({"coupon": coupon_serializer.data['code'], "data": serializer.data})

    def post(self, request, format=None):

        serializer = CartItemSerializer(
            data=request.data, context={"request": request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CartItemDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = CartItem.objects.all()
    serializer_class = ListCartItemSerializer
    lookup_field = "id"
