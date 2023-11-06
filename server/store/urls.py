from django.urls import path
from . import views

urlpatterns = [
    path("", views.ProductView.as_view(), name="product"),
    path("rate/", views.RateView.as_view(), name="rate"),
    path("reviews/", views.ReviewView.as_view(), name="reviews"),
    path("wishlist/", views.WishListView.as_view(), name="wishlist"),
    path("wishlist/<int:id>/", views.WishListDetailView.as_view(), name="wishlist"),
]
