from rest_framework import generics, status
from .models import Cart, CartItem
from .serializers import CartSerializer, CartItemSerializer, ListCartItemSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
import stripe
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404


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
        if cart.coupon:
            coupon_id = cart.coupon
            coupon = stripe.Coupon.retrieve(coupon_id)
            data = {
                'code': coupon['name'],
                'discount_amount': coupon['amount_off'],
                'min_total': coupon['metadata']['min_total'],
                'discount_type': coupon['metadata']['type'],
            }
        else:
            data = None
        return Response({'coupon_data': data, "cart_item": serializer.data})

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
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(cart_id__user_id=self.request.user)


class CartItemDeleteAPIVew(APIView):
    # Delete a Cart item  by product id

    def delete(self, request, id):
        cart_item = get_object_or_404(
            CartItem, product_id=id, cart_id__user_id=request.user)
        cart_item.delete()
        return Response({"message": "Product deleted successfully!"}, status=status.HTTP_204_NO_CONTENT)
