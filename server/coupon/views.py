from .serializers import *
from .models import *
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAdminUser


class CouponView(ListAPIView):
    queryset = Coupon.objects.all()
    serializer_class = CouponSerializer
    permission_classes = [IsAdminUser]
