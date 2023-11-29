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
from cart.serializers import CartSerializer


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
            if cart.coupon == coupon:
                return Response({"message": "Coupon already applied"}, status=status.HTTP_201_CREATED)
            else:
                cart.coupon = coupon
                cart.save()
                return Response({'message': "Coupon applied successfully", "copyright": " © Mahmoud-orabi 😁"}, status=status.HTTP_200_OK)
        except Coupon.DoesNotExist:
            return Response({'error': 'Coupon not is valid'}, status=status.HTTP_406_NOT_ACCEPTABLE)
