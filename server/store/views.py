from rest_framework import viewsets, generics
from .models import *
from .serializers import *
from django.db.models import Q


class BrandViewSet(viewsets.ModelViewSet):
    queryset = Brand.objects.all()
    serializer_class = BrandSerializer


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class ColorViewSet(viewsets.ModelViewSet):
    queryset = Color.objects.all()
    serializer_class = ColorSerializer


class SizeViewSet(viewsets.ModelViewSet):
    queryset = Size.objects.all()
    serializer_class = SizeSerializer


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductListSerializer

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return ProductDetailSerializer
        return ProductListSerializer

    def get_queryset(self):
        queryset = super().get_queryset()

        # Apply filters based on query parameters
        color = self.request.query_params.get('color')
        price_min = self.request.query_params.get('price_min')
        price_max = self.request.query_params.get('price_max')
        brand = self.request.query_params.get('brand')
        category = self.request.query_params.get('category')
        size = self.request.query_params.get('size')

        # Build filter expressions
        filters = Q()

        if color:
            filters &= Q(colors__name=color.title())

        if price_min:
            filters &= Q(price__gte=price_min)

        if price_max:
            filters &= Q(price__lte=price_max)

        if brand:
            filters &= Q(brand__name=brand.title())

        if category:
            filters &= Q(category__name=category.title())

        if size:
            filters &= Q(sizes__size=size.upper())

        return queryset.filter(filters)


class BestSellerView(generics.ListAPIView):
    queryset = Product.objects.all().order_by("-selled")
    serializer_class = ProductListSerializer

    def get_queryset(self):
        queryset = super().get_queryset()

        # Apply filters based on query parameters
        color = self.request.query_params.get('color')
        price_min = self.request.query_params.get('price_min')
        price_max = self.request.query_params.get('price_max')
        brand = self.request.query_params.get('brand')
        category = self.request.query_params.get('category')
        size = self.request.query_params.get('size')

        # Build filter expressions
        filters = Q()

        if color:
            filters &= Q(colors__name=color.title())

        if price_min:
            filters &= Q(price__gte=price_min)

        if price_max:
            filters &= Q(price__lte=price_max)

        if brand:
            filters &= Q(brand__name=brand.title())

        if category:
            filters &= Q(category__name=category.title())

        if size:
            filters &= Q(sizes__size=size.upper())

        return queryset.filter(filters)


class WishListViewSet(viewsets.ModelViewSet):
    queryset = WishList.objects.all()
    serializer_class = WishListSerializer


class EvaluationViewSet(viewsets.ModelViewSet):
    queryset = Evaluation.objects.all()
    serializer_class = EvaluationSerializer


class ImageViewSet(viewsets.ModelViewSet):
    queryset = Image.objects.all()
    serializer_class = ImageSerializer
