from django.urls import path
from .views import CouponView, ApplyCouponAPIView

urlpatterns = [
    path('', CouponView.as_view(), name="coupon"),
    path('apply_coupon/', ApplyCouponAPIView.as_view(), name="apply-coupon"),
]
