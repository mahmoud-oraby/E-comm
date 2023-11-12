from django.urls import path
from . import views

urlpatterns = [
    path("", views.ProductView.as_view(), name="product"),
    path("evaluation/", views.EvaluationView.as_view(), name="reviews-rate"),
    path("wishlist/", views.WishListAPIView.as_view(), name="wishlist"),
    path("wishlist/<int:id>/", views.WishListDetailView.as_view(), name="wishlist"),
]
