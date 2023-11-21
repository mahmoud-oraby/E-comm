from rest_framework import serializers
from .models import ShippingAddress


class ShippingAddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShippingAddress
        fields = "__all__"

    def create(self, validated_data):
        user = self.context["request"].user
        address, created = ShippingAddress.objects.get_or_create(
            user=user, **validated_data)
        return address
