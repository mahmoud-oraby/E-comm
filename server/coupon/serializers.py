from rest_framework import serializers
from .models import *


class CouponSerializer(serializers.ModelSerializer):
    class Meta:
        model = Coupon
        exclude = ["created_at", "updated_at"]
