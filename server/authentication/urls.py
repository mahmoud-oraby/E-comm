from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from .views import (RegisterView, RequestPasswordResetEmailView,
                    PasswordTokenCheckAPIView, ChangePasswordView)

urlpatterns = [
    path("register/", RegisterView.as_view(), name='register'),
    path("change_password/", ChangePasswordView.as_view(), name='change-password'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('reset_password/', RequestPasswordResetEmailView.as_view(),
         name='password-reset'),
    path("reset_password/<uidb64>/<token>/",
         PasswordTokenCheckAPIView.as_view(), name="Password-reset-confirm"),
    path("password_reset_complete/", PasswordTokenCheckAPIView.as_view(),
         name="password-reset-complete")
]
