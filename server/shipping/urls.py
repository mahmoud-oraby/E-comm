from django.urls import path, include
from rest_framework import routers
from .views import ShippingAddressView, SetDefaultAddress

router = routers.DefaultRouter()
router.register(r'', ShippingAddressView)

urlpatterns = [
    path('', include(router.urls)),
    path('set/<int:id>/', SetDefaultAddress.as_view(), name="set-default-address")
]
