# from rest_framework import generics, permissions, response, status
# from .models import *
# from .serializers import *
# from .permissions import IsAdminOrReadOnly
# from django.db.models import Q
# from rest_framework.views import APIView


# class ProductView(generics.ListCreateAPIView):
#     queryset = Product.objects.all()
#     serializer_class = ProductSerializer
#     permission_classes = [IsAdminOrReadOnly]

#     def get_queryset(self):
#         queryset = super().get_queryset()

#         # Filter brand
#         brand_name = self.request.query_params.get('brand', None)
#         if brand_name is not None:
#             queryset = queryset.filter(Q(brand__name__icontains=brand_name))

#         # Filter by price range
#         min_price = self.request.query_params.get('min_price', None)
#         max_price = self.request.query_params.get('max_price', None)
#         if (min_price is not None and max_price is not None):
#             queryset = queryset.filter(Q(price__range=(min_price, max_price)))

#         # Filter by available
#         available = self.request.query_params.get("available", None)
#         if available:
#             queryset = queryset.filter(available=(available.lower() == 'true'))

#         # Filter by color
#         color = self.request.query_params.get("color", None)
#         if color:
#             queryset = queryset.filter(colors__name=color.title())

#         # Filter by best seller
#         bestseller = self.request.query_params.get("bestseller", None)
#         if bestseller:
#             bestseller = int(bestseller)
#             print(type(bestseller))
#             queryset = queryset.order_by("-selled")[0: bestseller]
#         return queryset


# class EvaluationView(generics.ListCreateAPIView):
#     queryset = Evaluation.objects.all()
#     serializer_class = EvaluationSerializer
#     permission_classes = [permissions.IsAuthenticatedOrReadOnly]

#     # def perform_create(self, serializer):
#     #     user = User.objects.get(username=self.request.user)
#     #     product = Product.objects.get(id=1)
#     #     serializer.save(user=user)


# class WishListAPIView(APIView):
#     permission_classes = [permissions.IsAuthenticated]

#     def get_queryset(self):
#         return WishList.objects.filter(user=self.request.user).order_by('-id')

#     def get(self, request, format=None):
#         queryset = self.get_queryset()
#         serializer = WishListDetailSerializer(
#             queryset, many=True)
#         return response.Response(serializer.data)

#     def post(self, request, format=None):
#         serializer = WishListSerializer(
#             data=request.data, context={"request": request})
#         if serializer.is_valid():
#             serializer.save()
#             return response.Response(serializer.data, status=status.HTTP_201_CREATED)
#         else:
#             return response.Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# class WishListDetailView(generics.RetrieveDestroyAPIView):
#     queryset = WishList.objects.all()
#     serializer_class = WishListDetailSerializer
#     lookup_field = "id"
#     permission_classes = [permissions.IsAuthenticated]

#     def get_queryset(self):
#         return self.queryset.filter(user=self.request.user)


from rest_framework import viewsets
from .models import Brand, Category, Color, Size, Product, Evaluation, WishList
from .serializers import (
    BrandSerializer,
    CategorySerializer,
    ColorSerializer,
    SizeSerializer,
    ProductSerializer,
    EvaluationSerializer,
    WishListSerializer,
)
from rest_framework import mixins, response, status


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


class EvaluationViewSet(viewsets.ModelViewSet):
    queryset = Evaluation.objects.all()
    serializer_class = EvaluationSerializer


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    # def create(self, request, *args, **kwargs):
    #     serializer = self.get_serializer(data=request.data)
    #     serializer.is_valid(raise_exception=True)
    #     product = serializer.save()

    #     # أي عمليات إضافية ترغب في القيام بها بعد إنشاء المنتج هنا

    #     return response.Response(serializer.data, status=status.HTTP_201_CREATED)


class WishListViewSet(viewsets.ModelViewSet):
    queryset = WishList.objects.all()
    serializer_class = WishListSerializer
