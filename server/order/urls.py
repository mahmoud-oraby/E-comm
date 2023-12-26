from django.urls import path
from .views import OrderCreateView, OrderListView
app_name = "order"

urlpatterns = [
    path('', OrderCreateView.as_view(), name='create-order'),
    path('list/', OrderListView.as_view(), name='list-order'),
]
