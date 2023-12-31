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
    image = serializers.SerializerMethodField()
    class Meta:
        model = Product
        fields = ["id", "title", "price", "image"]
        
    def get_image(self,obj):
        return self.context['request'].build_absolute_uri(obj.image.url) if obj.image else None
    
    


class WishListGetSerializer(serializers.ModelSerializer):
    product = ProductSerializer()

    class Meta:
        model = WishListItem
        fields = ["id", "product", 'created_at']
