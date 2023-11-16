from rest_framework import serializers
from authentication.serializers import UserSerializer
from .models import Product, Brand, Category, Color, Size, Evaluation, WishList


# class BrandSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Brand
#         fields = '__all__'


# class CategorySerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Category
#         fields = '__all__'


# class ColorSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Color
#         fields = '__all__'


# class SizeSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Size
#         fields = ['size',]


# class EvaluationSerializer(serializers.ModelSerializer):
#     user = serializers.SerializerMethodField()
#     product = serializers.SerializerMethodField()

#     class Meta:
#         model = Evaluation
#         fields = '__all__'

#     def create(self, validated_data):
#         # Get the user and product objects from the context or the data
#         user = self.context['request'].user
#         product = Product.objects.get(id=self.initial_data['product'])
#         # Create the evaluation object with the user and product
#         evaluation = Evaluation.objects.create(
#             user=user, product=product, **validated_data)
#         return evaluation

#     def get_user(self, obj):
#         user = obj.user
#         if user:
#             return user.username

#     def get_product(self, obj):
#         product = obj.product
#         if product:
#             return product.title


# class WishListSerializer(serializers.ModelSerializer):
#     user = serializers.SerializerMethodField()

#     class Meta:
#         model = WishList
#         fields = '__all__'

#     def get_user(self, obj):
#         return str(obj.user)

#     def create(self, validated_data):
#         user = self.context['request'].user
#         product = validated_data.pop("product")
#         wishlist, created = WishList.objects.get_or_create(
#             user=user, product=product)
#         return wishlist

#     def to_representation(self, instance):
#         # Remove a user from json response
#         representation = super().to_representation(instance)
#         representation.pop('user')
#         return representation


# class WishListDetailSerializer(WishListSerializer):
#     product = serializers.SerializerMethodField()
#     user = serializers.SerializerMethodField()

#     class Meta(WishListSerializer.Meta):
#         fields = WishListSerializer.Meta.fields

#     def get_user(self, obj):
#         return str(obj.user)

#     def get_product(self, obj):
#         return str(obj.product.title)


# class ProductSerializer(serializers.ModelSerializer):
#     brand = BrandSerializer(read_only=True)
#     category = serializers.SerializerMethodField()
#     colors = ColorSerializer(many=True, read_only=True)
#     sizes = serializers.SerializerMethodField()
#     evaluation = serializers.SerializerMethodField()

#     class Meta:
#         model = Product
#         fields = '__all__'

#     def get_evaluation(self, obj):

#         ratings = obj.reviews.all()
#         rate_list = [rating.rate for rating in ratings]
#         return sum(rate_list)/len(rate_list) if len(rate_list) > 0 else 0

#     def get_sizes(self, obj):

#         sizes = obj.sizes.all()
#         size_list = []
#         for size in sizes:
#             size_dict = {
#                 'size': size.size,
#             }
#             size_list.append(size_dict['size'])
#         return size_list

#     def get_category(self, obj):

#         category = str(obj.category)

#         return category

#     def get_reviews(self, obj):
#         reviews = obj.reviews.all()
#         review_list = []
#         for review in reviews:
#             review_dict = {
#                 'user': review.user.username,
#                 'review': review.content,
#                 'product': review.product.title, }
#             review_list.append(review_dict)
#         return review_list


class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = '__all__'


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
        fields = '__all__'


class EvaluationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Evaluation
        fields = '__all__'


class ProductSerializer(serializers.ModelSerializer):
    brand = BrandSerializer()
    category = CategorySerializer()
    colors = ColorSerializer(many=True)
    sizes = SizeSerializer(many=True)

    class Meta:
        model = Product
        fields = '__all__'

    def create(self, validated_data):
        brand_data = validated_data.pop('brand')
        category_data = validated_data.pop('category')
        colors_data = validated_data.pop('colors')
        sizes_data = validated_data.pop('sizes')
        print(brand_data)
        brand, created = Brand.objects.get_or_create(**brand_data)
        category = Category.objects.create(**category_data)

        product = Product.objects.create(
            brand=brand,
            category=category,
            **validated_data
        )

        colors = [Color.objects.create(**color_data)
                  for color_data in colors_data]
        sizes = [Size.objects.create(**size_data) for size_data in sizes_data]

        # Set the many-to-many relationship using the 'set' method
        product.colors.set(colors)
        # Set the many-to-many relationship using the 'set' method
        product.sizes.set(sizes)

        return product


class WishListSerializer(serializers.ModelSerializer):
    class Meta:
        model = WishList
        fields = '__all__'
