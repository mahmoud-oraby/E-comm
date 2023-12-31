
from rest_framework import viewsets, generics
from .models import *
from .serializers import *
from django.db.models import Q
from rest_framework.response import Response
from rest_framework.views import APIView
from django.db.models import Avg


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
        colors = self.request.query_params.getlist('color')
        price_min = self.request.query_params.get('price_min')
        price_max = self.request.query_params.get('price_max')
        brands = self.request.query_params.getlist('brand')
        categories = self.request.query_params.getlist('category')
        sizes = self.request.query_params.getlist('size')

        filters = Q()

        if colors:
            filters &= Q(colors__name__in=[color for color in colors])

        if price_min:
            filters &= Q(price__gte=price_min)

        if price_max:
            filters &= Q(price__lte=price_max)

        if brands:
            filters &= Q(brand__name__in=[brand.title() for brand in brands])

        if categories:
            filters &= Q(category__name__in=[
                         category.title() for category in categories])

        if sizes:
            filters &= Q(sizes__size__in=[size.upper() for size in sizes])

        queryset = queryset.filter(filters)
        # Apply sorting
        sort_by = self.request.query_params.get('sort_by')

        if sort_by == '-title':
            queryset = queryset.order_by('-title')
        if sort_by == '-price':
            queryset = queryset.order_by('-price')
        if sort_by == '-reviews':
            queryset = queryset.annotate(
                avg_rating=Avg('reviews__rate')).order_by('-avg_rating')

        return queryset


class BestSellerView(generics.ListAPIView):
    queryset = Product.objects.all().order_by("-selled")
    serializer_class = ProductListSerializer

    def get_queryset(self):
        queryset = super().get_queryset()

        # Apply filters based on query parameters
        colors = self.request.query_params.getlist('color')
        price_min = self.request.query_params.get('price_min')
        price_max = self.request.query_params.get('price_max')
        brands = self.request.query_params.getlist('brand')
        categories = self.request.query_params.getlist('category')
        sizes = self.request.query_params.getlist('size')

        filters = Q()

        if colors:
            filters &= Q(colors__name__in=[color.title() for color in colors])

        if price_min:
            filters &= Q(price__gte=price_min)

        if price_max:
            filters &= Q(price__lte=price_max)

        if brands:
            filters &= Q(brand__name__in=[brand.title() for brand in brands])

        if categories:
            filters &= Q(category__name__in=[
                         category.title() for category in categories])

        if sizes:
            filters &= Q(sizes__size__in=[size.upper() for size in sizes])

        return queryset.filter(filters)


class EvaluationViewSet(viewsets.ModelViewSet):
    queryset = Evaluation.objects.all()
    serializer_class = EvaluationSerializer

    def get_queryset(self):
        # Return evaluations of the current authenticated user
        return Evaluation.objects.filter(user=self.request.user)


class ImageViewSet(viewsets.ModelViewSet):
    queryset = Image.objects.all()
    serializer_class = ImageSerializer


class DataAPIView(APIView):
    def get(self, request):
        brands = Brand.objects.all()
        colors = Color.objects.all()
        categories = Category.objects.all()
        sizes = Size.objects.all()

        serializer = DataSerializer({
            'brands': brands,
            'colors': colors,
            'categories': categories,
            'sizes': sizes
        })

        return Response(serializer.data)
