from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
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


class WishListDeleteAPIVew(APIView):
    def delete(self, request, id):
        wishlist_item = get_object_or_404(WishListItem, product_id=id)
        wishlist_item.delete()
        return Response({"message": "Product deleted successfully!"}, status=status.HTTP_204_NO_CONTENT)
