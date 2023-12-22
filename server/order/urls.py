from django.urls import path
from .views import OrderListCreateView, OrderListView
app_name = "order"

urlpatterns = [
    path('', OrderListCreateView.as_view(), name='order-list'),
    path('list/', OrderListView.as_view(), name='order-list--'),
]
