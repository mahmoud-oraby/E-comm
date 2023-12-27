from rest_framework import serializers
from .models import Order, ProductOrder
from shipping.models import ShippingAddress
from cart.models import Cart, CartItem
from django.db.models import F, Sum
from .utils import generate_random
from store.serializers import ProductDetailSerializer
from shipping.serializer import ShippingAddressListSerializer


class ProductOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductOrder
        fields = '__all__'


class OrderCreateSerializers(serializers.ModelSerializer):
    shipping = serializers.CharField(required=False)
    product = ProductOrderSerializer(many=True, required=False)

    class Meta:
        model = Order
        fields = "__all__"

    def create(self, validated_data):
        products_data = validated_data.pop('product', [])
        user = self.context['request'].user
        cart = Cart.objects.get(user=user)
        try:
            shipping = ShippingAddress.objects.get(
                user=user, default_address=True)
        except ShippingAddress.DoesNotExist:
            return {'message': 'Please add a primary address'}

        total = CartItem.objects.filter(cart=cart).aggregate(
            total_price=Sum(F('product__price') * F('quantity')))['total_price']
        if total:
            products = CartItem.objects.filter(cart=cart)
            order = Order.objects.create(
                customer_name=user, cart=cart, order_id=generate_random(), total_price=total, shipping=shipping)
            for product in products:
                product_order, created = ProductOrder.objects.get_or_create(
                    product_name=product.product, price=product.product.price, quantity=product.quantity, image=product.product.image)
                order.product.add(product_order)

            CartItem.objects.filter(cart=cart).delete()
        else:
            raise serializers.ValidationError("Cart is empty")
        return order


class CustomShippingSerializer(serializers.ModelSerializer):
    class Meta:
        list_serializer_class = ShippingAddressListSerializer
        model = ShippingAddress
        fields = ['first_name', 'last_name', 'email', 'address1']


class OrderGetSerializer(serializers.ModelSerializer):
    product = serializers.SerializerMethodField()
    shipping = CustomShippingSerializer()

    class Meta:
        model = Order
        fields = '__all__'

    def get_product(self, obj):
        products = obj.product.all()
        product_list = []
        for item in products:
            product_dict = {
                "product_name": item.product_name,
                "price": item.price,
                "image": item.image.url,
            }
            product_list.append(product_dict)
        return product_list
