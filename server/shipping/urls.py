from django.urls import path, include
from rest_framework import routers
from .views import ShippingAddressView

router = routers.DefaultRouter()
router.register(r'', ShippingAddressView)

urlpatterns = [
    path('', include(router.urls))
]
