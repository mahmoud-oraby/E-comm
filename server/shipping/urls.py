from django.urls import path
from .views import ShippingAddressView

urlpatterns = [
    path('', ShippingAddressView.as_view(), name="shipping"),
]
