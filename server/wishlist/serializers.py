from rest_framework import serializers
from .models import WishList, WishListItem
from store.models import Product


class WishListSerializer(serializers.ModelSerializer):
    class Meta:
        model = WishList
        fields = "__all__"


class WishListItemSerializer(serializers.ModelSerializer):
    wishlist = serializers.CharField(required=False)

    class Meta:
        model = WishListItem
        fields = "__all__"

    def create(self, validated_data):
        try:
            wishlist = WishList.objects.get(user=self.context["request"].user)
        except WishList.DoesNotExist:
            wishlist = WishList.objects.create(
                user=self.context["request"].user)
        product = validated_data.pop("product", None)

        wishlist_item, created = WishListItem.objects.get_or_create(
            wishlist=wishlist, product=product)
        return wishlist_item


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ["id", "title", "price", "image"]


class WishListGetSerializer(serializers.ModelSerializer):
    product = ProductSerializer()

    class Meta:
        model = WishList
        fields = ["id", "product"]
