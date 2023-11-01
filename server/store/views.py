from rest_framework import generics, permissions
from rest_framework.response import Response
from .models import *
from .serializers import *
from .permissions import IsAdminOrReadOnly
from django.db.models import Q


class ProductView(generics.ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAdminOrReadOnly]

    def get_queryset(self):
        queryset = super().get_queryset()

        # Filter brand
        brand_name = self.request.query_params.get('brand', None)
        if brand_name is not None:
            queryset = queryset.filter(Q(brand__name__icontains=brand_name))

        # Filter by price range
        min_price = self.request.query_params.get('min_price', None)
        max_price = self.request.query_params.get('max_price', None)
        if (min_price is not None and max_price is not None):
            queryset = queryset.filter(Q(price__range=(min_price, max_price)))

        # Filter by available
        available = self.request.query_params.get("available", None)
        if available:
            queryset = queryset.filter(available=(available.lower() == 'true'))

        # Filter by color
        color = self.request.query_params.get("color", None)
        if color:
            queryset = queryset.filter(colors__name=color.title())

        # Filter by best seller
        bestseller = self.request.query_params.get("bestseller", None)
        if bestseller:
            bestseller = int(bestseller)
            print(type(bestseller))
            queryset = queryset.order_by("-selled")[0: bestseller]
        return queryset


class RateView(generics.ListCreateAPIView):
    queryset = Rate.objects.all()
    serializer_class = RateSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class ReviewView(generics.ListCreateAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
