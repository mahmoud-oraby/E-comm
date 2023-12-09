from rest_framework import serializers
from .models import ShippingAddress
from rest_framework import status


class ShippingAddressCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShippingAddress
        exclude = ["default_address"]

    def create(self, validated_data):
        user = self.context["request"].user
        existing_default_address = ShippingAddress.objects.filter(
            user=user,  **validated_data).exists()

        shipping = ShippingAddress.objects.filter(user=user,
                                                  default_address=True).exists()

        if not existing_default_address:
            if shipping:
                shipping = ShippingAddress.objects.get(
                    user=user, default_address=True)
                shipping.default_address = False
                shipping.save()

            address, created = ShippingAddress.objects.get_or_create(
                user=user, default_address=True, **validated_data)
            return address
        else:
            raise serializers.ValidationError(
                "Error: Default address already exists.")


class ShippingAddressListSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShippingAddress
        fields = "__all__"
