from django.urls import path
from .views import create_checkout_session, create_checkout_session_webhook

urlpatterns = [
    path('', create_checkout_session, name="checkout"),
    path('checkout_webhook/', create_checkout_session_webhook,
         name="create-checkout-session-webhook"),
]
