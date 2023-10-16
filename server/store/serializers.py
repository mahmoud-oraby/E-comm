from rest_framework import serializers
from .models import Product, Brand, Rate, Category, Color


class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = '__all__'


class RateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rate
        fields = '__all__'


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class ColorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Color
        fields = '__all__'


class ProductSerializer(serializers.ModelSerializer):
    rate = serializers.SerializerMethodField()
    brand = BrandSerializer(read_only=False)
    category = CategorySerializer(read_only=False)
    colors = ColorSerializer(many=True)

    class Meta:
        model = Product
        fields = '__all__'

    def get_rate(self, obj):

        ratings = obj.ratings.all()
    # Convert the ratings to a list of dictionaries
        rate_list = []
        for rating in ratings:
            rate_dict = {
                'id': rating.id,
                'user_name': rating.user.username,
                'product_name': rating.product.title,
                'rate': rating.rate
            }
            rate_list.append(rate_dict)
        return rate_list
