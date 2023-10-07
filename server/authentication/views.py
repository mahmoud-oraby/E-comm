from rest_framework import generics, status, views
from .models import User
from .serializers import RegisterSerializer, EmailVerificationSerializer
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
from .utils import Utils
import jwt
from django.conf import settings

# Create your views here.


class RegisterView(generics.GenericAPIView):
    serializer_class = RegisterSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        user = User.objects.get(email=serializer.data['email'])
        token = RefreshToken.for_user(user).access_token

        current_site = get_current_site(request).domain
        relative_link = reverse("email_verify")
        absolute_url = f"http://{current_site}{relative_link}?token={token}"
        email_body = f"Hi {user.username} Use link below to verify your email \n {absolute_url}"
        data = {"email_body": email_body, "to_email": [user.email,],
                "email_subject": "Verify your email"}
        Utils.send_email(data)

        return Response(serializer.data, status=status.HTTP_201_CREATED)


class VerifyEmail(views.APIView):

    serializer_class = EmailVerificationSerializer

    def get(self, request):
        token = request.GET.get("token")
        try:
            payload = jwt.decode(
                token, settings.SECRET_KEY, algorithms=["HS256"])
            user = User.objects.get(id=payload['user_id'])
            if not user.is_verified:
                user.is_verified = True
                user.save()
            return Response({"email": "Success Activated"}, status=status.HTTP_200_OK)
        except jwt.ExpiredSignatureError as identifier:
            raise Exception('Activation Link Expired',
                            status=status.HTTP_400_BAD_REQUEST)
        except jwt.exceptions.DecodeError as identifier:
            raise Exception('Invalid token',
                            status=status.HTTP_400_BAD_REQUEST)
