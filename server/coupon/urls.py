from django.urls import path
from .views import CouponView, ApplyCouponAPIView, DeleteCouponFormCart

urlpatterns = [
    path('', CouponView.as_view(), name="create-coupon"),
    path('apply_coupon/', ApplyCouponAPIView.as_view(), name="apply-coupon"),
    path('delete_coupon/', DeleteCouponFormCart.as_view(), name="delete-coupon"),
]
