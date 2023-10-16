from django.urls import path
from . import views

urlpatterns = [
    path("", views.ProductView.as_view(), name="product"),
    path("rate/", views.RateView.as_view(), name="rate"),
]
