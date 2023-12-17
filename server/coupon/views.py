from .serializers import *
from .models import *
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from django.utils import timezone
from rest_framework import status
from cart.models import Cart
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView


class CouponView(ListAPIView):
    queryset = Coupon.objects.all()
    serializer_class = CouponSerializer
    permission_classes = [IsAdminUser]


class ApplyCouponAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, format=None):
        coupon_code = request.data.get("coupon_code")
        try:
            coupon = Coupon.objects.get(
                code=coupon_code, start_date__lte=timezone.now(), end_date__gte=timezone.now())
            user = request.user
            cart = get_object_or_404(Cart, user=user)
            cart_total = cart.get_cart_total()
            print('cart_total', cart_total)
            if cart_total >= coupon.min_total:
                if cart.coupon == coupon:
                    return Response({"message": "Coupon already applied"}, status=status.HTTP_201_CREATED)
                else:
                    cart.coupon = coupon
                    cart.save()
                    return Response({'message': "Coupon applied successfully"}, status=status.HTTP_200_OK)
            else:
                return Response({"message": f"Your order total must be {coupon.min_total} or more to apply this discount."}, status=status.HTTP_406_NOT_ACCEPTABLE)
        except Coupon.DoesNotExist:
            return Response({'error': 'Coupon not is valid'}, status=status.HTTP_406_NOT_ACCEPTABLE)


class DeleteCouponFormCart(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, format=None):
        cart = get_object_or_404(Cart, user=request.user)
        cart.coupon = None
        cart.save()
        return Response({'message': 'Coupon deleted'}, status=status.HTTP_200_OK)
