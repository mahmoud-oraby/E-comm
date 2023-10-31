from rest_framework import serializers
from .models import Cart, CartItem
from django.db.models import Q


class CartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cart
        fields = ('id', 'user')
        read_only_fields = ['id']


class CartItemSerializer(serializers.ModelSerializer):
    cart = serializers.SerializerMethodField()

    class Meta:
        model = CartItem
        fields = ('cart', 'product', 'quantity')
        read_only_fields = ['id']

    def create(self, validated_data):
        cart = validated_data.pop("cart", [])
        auth_user = self.context['request'].user
        cart_obj = Cart.objects.get(user=auth_user)
        # check if cart item is exists quantity += Validate_data["quantity"] else create cart item
        try:
            cart_item = CartItem.objects.get(
                Q(cart=cart_obj) and Q(product__title=validated_data["product"]))
            cart_item.quantity += validated_data["quantity"]
            cart_item.save()
            return cart_item
        except CartItem.DoesNotExist:
            cart_item = CartItem.objects.create(
                cart=cart_obj, **validated_data)
            return cart_item

    def get_cart(self, obj):
        return str(obj.cart)
