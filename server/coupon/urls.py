from django.urls import path
from .views import CouponView

urlpatterns = [
    path('', CouponView.as_view(), name="coupon")
]
