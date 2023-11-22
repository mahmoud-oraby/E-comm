from django.urls import include, path
from rest_framework import routers
from .views import *

router = routers.DefaultRouter()
router.register(r'brands', BrandViewSet)
router.register(r'categories', CategoryViewSet)
router.register(r'colors', ColorViewSet)
router.register(r'sizes', SizeViewSet)
router.register(r'products', ProductViewSet)
router.register(r'evaluations', EvaluationViewSet)
router.register(r'wishlists', WishListViewSet)
router.register(r'images', ImageViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('product/best_seller/', BestSellerView.as_view(), name="best-seller"),
    path('product/data/', DataAPIView.as_view(), name="data")
]
