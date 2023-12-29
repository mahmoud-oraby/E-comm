from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from cart.models import Cart
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
import stripe


class CouponView(APIView):
    permission_classes = [IsAdminUser]

    def post(self, request, format=None):
        discount_type = request.data.get("type")
        if discount_type == "fixed":
            percent_off = None
            amount_off = request.data.get('amount')
        elif discount_type == "percentage":
            amount_off = None
            percent_off = request.data.get('percent')

        coupon = stripe.Coupon.create(
            amount_off=amount_off,
            percent_off=percent_off,
            currency="USD",
            duration="once",
            max_redemptions=request.data.get('limit'),
            redeem_by=request.data.get("expire"),
            name=request.data.get('code'),
            metadata={
                "min_total": request.data.get('min_total'),
                "type": request.data.get('type')
            }
        )
        return Response({"status": "SUCCESS", "couponId": coupon.id, 'coupon_name': coupon.name}, status=status.HTTP_201_CREATED)


class ApplyCouponAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, format=None):
        coupon_code = request.data.get("coupon_code")
        try:
            coupons = stripe.Coupon.list()
            coupon = [coupon for coupon in coupons if coupon.get(
                'name') == coupon_code][0]
            if not coupon or coupon.valid == False:
                 return Response({'error': 'Coupon not is valid'}, status=status.HTTP_406_NOT_ACCEPTABLE)

            user = request.user
            cart = get_object_or_404(Cart, user=user)
            cart_total = cart.get_cart_total()
            if cart_total >= int(coupon.metadata['min_total']):
                if cart.coupon == coupon.id:
                    return Response({"message": "Coupon already applied"}, status=status.HTTP_201_CREATED)
                else:
                    cart.coupon = coupon.id
                    cart.save()
                    return Response({'message': "Coupon applied successfully"}, status=status.HTTP_200_OK)
            else:
                return Response({"message": f"Your order total must be {coupon.metadata['min_total']} or more to apply this discount."}, status=status.HTTP_406_NOT_ACCEPTABLE)
        except:
            return Response({'error': 'Coupon not is valid'}, status=status.HTTP_406_NOT_ACCEPTABLE)


class DeleteCouponFormCart(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, format=None):
        cart = get_object_or_404(Cart, user=request.user)
        cart.coupon = None
        cart.save()
        return Response({'message': 'Coupon deleted'}, status=status.HTTP_200_OK)
