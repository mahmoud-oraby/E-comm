from rest_framework import serializers
from authentication.serializers import UserSerializer
from .models import Product, Brand, Rate, Category, Color, Size, Review


class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = '__all__'


class RateSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()
    product = serializers.SerializerMethodField()

    class Meta:
        model = Rate
        fields = '__all__'

    def get_user(self, obj):
        return obj.user.username

    def get_product(self, obj):
        product = obj.product
        if product:
            return product.title
        return None


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class ColorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Color
        fields = '__all__'


class SizeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Size
        fields = ['size',]


class ReviewSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()
    product = serializers.SerializerMethodField()

    class Meta:
        model = Review
        fields = '__all__'

    def get_user(self, obj):
        user = obj.user
        if user:
            return user.username

    def get_product(self, obj):
        product = obj.product
        if product:
            return product.title


class ProductSerializer(serializers.ModelSerializer):
    rate = serializers.SerializerMethodField()
    brand = BrandSerializer(read_only=False)
    category = serializers.SerializerMethodField()
    colors = ColorSerializer(many=True)
    sizes = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = '__all__'

    def get_rate(self, obj):

        ratings = obj.ratings.all()
        rate_list = [rating.rate for rating in ratings]
        return sum(rate_list)/len(rate_list) if len(rate_list) > 0 else 0

    def get_sizes(self, obj):

        sizes = obj.sizes.all()
        size_list = []
        for size in sizes:
            size_dict = {
                'size': size.size,
            }
            size_list.append(size_dict['size'])
        return size_list

    def get_category(self, obj):

        category = obj.category
        if category:
            return category.name
        return None
