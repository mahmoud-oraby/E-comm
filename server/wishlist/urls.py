from django.urls import path
from .views import *

urlpatterns = [
    path('', WishListView.as_view(), name='wishlist'),
    path('item/', WishListItemView.as_view(), name='wishlist_item'),
    path('item/<int:id>/',
         WishListDeleteAPIVew.as_view(), name='delete-wishlist'),
]
