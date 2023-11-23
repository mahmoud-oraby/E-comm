from rest_framework import generics
from rest_framework import permissions
from .models import *
from .serializers import *


class WishListView(generics.ListCreateAPIView):
    queryset = WishList.objects.all()
    serializer_class = WishListSerializer
    pagination_class = None
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return WishList.objects.filter(user=self.request.user)


class WishListItemView(generics.ListCreateAPIView):
    queryset = WishListItem.objects.all()
    serializer_class = WishListItemSerializer
    pagination_class = None

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return WishListGetSerializer
        return WishListItemSerializer

    def get_queryset(self):
        return self.queryset.filter(wishlist_id__user_id=self.request.user)
