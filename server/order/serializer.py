from rest_framework import serializers
from .models import Order
from shipping.models import ShippingAddress
from cart.models import Cart, CartItem
from django.db.models import F, Sum
from .utils import generate_random


class OrderSerializers(serializers.ModelSerializer):
    shipping = serializers.CharField(required=False)

    class Meta:
        model = Order
        fields = "__all__"

    def create(self, validated_data):
        user = self.context['request'].user
        cart = Cart.objects.get(user=user)
        try:
            shipping = ShippingAddress.objects.get(
                user=user, primary_address=True)
        except ShippingAddress.DoesNotExist:
            return {'message': 'Please add a primary address'}

        total = CartItem.objects.filter(cart=cart).aggregate(
            total_price=Sum(F('product__price') * F('quantity')))['total_price']
        if total:
            order = Order.objects.create(
                customer_name=user, cart=cart, order_id=generate_random(), total_price=total, shipping=shipping)
            CartItem.objects.all().delete()
        else:
            raise serializers.ValidationError("Cart is empty")
        return order
