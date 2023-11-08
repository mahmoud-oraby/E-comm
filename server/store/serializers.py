from rest_framework import serializers
from authentication.serializers import UserSerializer
from .models import Product, Brand, Rate, Category, Color, Size, Review, WishList


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


class WishListSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()

    class Meta:
        model = WishList
        fields = '__all__'

    def get_user(self, obj):
        return str(obj.user)

    def create(self, validated_data):
        user = self.context['request'].user
        product = validated_data.pop("product")
        wishlist, created = WishList.objects.get_or_create(
            user=user, product=product)
        return wishlist

    def to_representation(self, instance):
        # Remove a user from json response
        representation = super().to_representation(instance)
        representation.pop('user')
        return representation


class WishListDetailSerializer(WishListSerializer):
    product = serializers.SerializerMethodField()
    user = serializers.SerializerMethodField()

    class Meta(WishListSerializer.Meta):
        fields = WishListSerializer.Meta.fields

    def get_user(self, obj):
        return str(obj.user)

    def get_product(self, obj):
        return str(obj.product.title)


class ProductSerializer(serializers.ModelSerializer):
    rate = serializers.SerializerMethodField()
    brand = BrandSerializer(read_only=False)
    category = serializers.SerializerMethodField()
    colors = ColorSerializer(many=True)
    sizes = serializers.SerializerMethodField()
    reviews = serializers.SerializerMethodField()

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

        category = str(obj.category)

        return category

    def get_reviews(self, obj):
        reviews = obj.reviews.all()
        review_list = []
        for review in reviews:
            review_dict = {
                'user': review.user.username,
                'review': review.content,
                'product': review.product.title, }
            review_list.append(review_dict)
        return review_list
