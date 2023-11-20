# from django.urls import path
# from . import views

# urlpatterns = [
#     path("", views.ProductView.as_view(), name="product"),
#     path("evaluation/", views.EvaluationView.as_view(), name="reviews-rate"),
#     path("wishlist/", views.WishListAPIView.as_view(), name="wishlist"),
#     path("wishlist/<int:id>/", views.WishListDetailView.as_view(), name="wishlist"),
# ]

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
    path('product/best_seller/', BestSellerView.as_view(), name="best-seller")
]
