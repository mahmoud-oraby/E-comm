from django.urls import path
from . import views

urlpatterns = [
    path("", views.CartList.as_view(), name="cart"),
    path("cart_item/", views.CartItemListCreateAPIView.as_view(),
         name="cart-item"),
    path("cart_item/<int:id>/", views.CartItemDetailView.as_view(),
         name="cart-item-detail"),

]
