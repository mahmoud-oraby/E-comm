from rest_framework import serializers
from cart.models import CartItem
from .models import (Product, Brand, Category, Color,
                     Size, Evaluation, Image)
from django.conf import settings
from django.contrib.sites.shortcuts import get_current_site
from rest_framework.utils import model_meta
from wishlist.models import WishList, WishListItem


class BrandSerializer(serializers.ModelSerializer):
    products = serializers.SerializerMethodField()

    class Meta:
        model = Brand
        fields = ["name", "products"]

    def get_products(self, obj):
        return obj.product.count()


class CategorySerializer(serializers.ModelSerializer):
    products = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = ["name", "products"]

    def get_products(self, obj):
        return obj.product.count()


class ColorSerializer(serializers.ModelSerializer):
    products = serializers.SerializerMethodField()

    class Meta:
        model = Color
        fields = ["name", "products"]

    def get_products(self, obj):
        return obj.product.count()


class SizeSerializer(serializers.ModelSerializer):
    products = serializers.SerializerMethodField()

    class Meta:
        model = Size
        fields = ["size", "products"]

    def get_products(self, obj):
        return obj.product.count()


class EvaluationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Evaluation
        fields = '__all__'


class ImageSerializer(serializers.ModelSerializer):

    class Meta:
        model = Image
        fields = '__all__'

# # class ProductCreateSerializer(serializers.ModelSerializer):
#     brand = BrandSerializer()
#     category = CategorySerializer()
#     colors = ColorSerializer(many=True)
#     sizes = SizeSerializer(many=True)
#     images = serializers.SerializerMethodField()

#     class Meta:
#         model = Product
#         fields = "__all__"

#     def get_images(self, obj):
#         images = obj.images.all()
#         current_site = get_current_site(self.context['request']).domain
#         image_list = []
#         for img in images:
#             image_list.append(
#                 f'http://{current_site}{settings.MEDIA_URL + str(img)}')
#         return image_list

#     def create(self, validated_data):
#         brand_data = validated_data.pop('brand')
#         category_data = validated_data.pop('category')
#         colors_data = validated_data.pop('colors')
#         sizes_data = validated_data.pop('sizes')
#         brand, created = Brand.objects.get_or_create(**brand_data)
#         category, created = Category.objects.get_or_create(**category_data)

#         product = Product.objects.create(
#             brand=brand,
#             category=category,
#             **validated_data
#         )

#         colors = [Color.objects.create(**color_data)
#                   for color_data in colors_data]
#         sizes = [Size.objects.create(**size_data) for size_data in sizes_data]

#         product.colors.set(colors)
#         product.sizes.set(sizes)

#         return product


class ProductListSerializer(serializers.ModelSerializer):
    is_in_cart = serializers.SerializerMethodField()
    is_in_wishlist = serializers.SerializerMethodField()
    evaluation = serializers.SerializerMethodField()
    evaluation_count = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = ["id", "title", "price", "discount", "description",
                  "label", "image", "is_in_cart", "is_in_wishlist", "selled", "evaluation", "evaluation_count"]

    def get_is_in_cart(self, obj):
        user = self.context['request'].user
        if user.is_authenticated:
            return CartItem.objects.filter(
                cart_id__user_id=self.context["request"].user, product=obj).exists()

        else:
            return False

    def get_is_in_wishlist(self, obj):
        user = self.context['request'].user
        if user.is_authenticated:
            wishlist = WishListItem.objects.filter(
                wishlist_id__user_id=self.context["request"].user, product=obj).exists()
            return wishlist
        else:
            return False

    def get_evaluation(self, obj):
        reviews = obj.reviews.all()
        rate_list = [rating.rate for rating in reviews]
        return sum(rate_list)/len(rate_list) if len(rate_list) > 0 else 0

    def get_evaluation_count(self, obj):
        reviews = obj.reviews.all()
        return len(reviews)


class ProductDetailSerializer(serializers.ModelSerializer):
    brand = serializers.StringRelatedField()
    category = serializers.StringRelatedField()
    colors = serializers.SerializerMethodField()
    sizes = serializers.SerializerMethodField()
    is_in_cart = serializers.SerializerMethodField()
    is_in_wishlist = serializers.SerializerMethodField()
    images = serializers.SerializerMethodField()
    evaluation = serializers.SerializerMethodField()
    reviews = serializers.SerializerMethodField()

    class Meta:
        model = Product
        exclude = ["created_at", "update_at", "active"]

    def get_is_in_cart(self, obj):
        user = self.context['request'].user
        if user.is_authenticated:
            return CartItem.objects.filter(
                cart_id__user_id=self.context["request"].user, product=obj).exists()

        else:
            return False

    def get_is_in_wishlist(self, obj):
        user = self.context['request'].user
        if user.is_authenticated:
            wishlist = WishListItem.objects.filter(
                wishlist_id__user_id=self.context["request"].user, product=obj).exists()
            return wishlist
        else:
            return False

    def get_images(self, obj):
        images = obj.images.all()
        current_site = get_current_site(self.context['request']).domain
        image_list = []
        for img in images:
            image_list.append(
                f'http://{current_site}{settings.MEDIA_URL + str(img)}')
        return image_list

    def get_colors(self, obj):
        colors = obj.colors.all()
        return [color.name for color in colors]

    def get_sizes(self, obj):
        sizes = obj.sizes.all()
        return [size.size for size in sizes]

    def get_reviews(self, obj):
        reviews = obj.reviews.all()
        review_list = []
        for review in reviews:
            review_dic = {
                "id": review.id,
                'rating': review.rate,
                'comment': review.content,
                'customer': review.user.username,
            }
            review_list.append(review_dic)
        return review_list

    def get_evaluation(self, obj):
        reviews = obj.reviews.all()
        rate_list = [rating.rate for rating in reviews]
        return sum(rate_list)/len(rate_list) if len(rate_list) > 0 else 0


class EvaluationSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()
    product = serializers.SerializerMethodField()

    class Meta:
        model = Evaluation
        fields = '__all__'

    def create(self, validated_data):
        user = self.context['request'].user
        product = Product.objects.get(id=self.initial_data['product'])
        # Create the evaluation object with the user and product
        try:
            evaluation = Evaluation.objects.get(user=user, product=product)
            raise serializers.ValidationError(
                "You have already evaluated this product")
        except Evaluation.DoesNotExist:
            evaluation = Evaluation.objects.create(
                user=user, product=product, **validated_data)
            return evaluation

    def get_user(self, obj):
        return str(obj.user)

    def get_product(self, obj):
        product = obj.product
        if product:
            return product.title


class DataSerializer(serializers.Serializer):
    brands = BrandSerializer(many=True)
    colors = ColorSerializer(many=True)
    categories = CategorySerializer(many=True)
    sizes = SizeSerializer(many=True)
