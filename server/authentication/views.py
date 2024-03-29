from rest_framework import generics, status, views, permissions
from .models import User
from .serializers import *
from rest_framework.response import Response
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
from .utils import Utils
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.encoding import smart_str, smart_bytes, DjangoUnicodeDecodeError
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.contrib.auth.hashers import check_password
# Create your views here.


class RegisterView(generics.GenericAPIView):
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class ChangePasswordView(views.APIView):
    def post(self, request):
        serializer = ChangePasswordSerializer(data=request.data)
        if serializer.is_valid():
            user = request.user
            old_password = serializer.data.get('old_password')
            new_password = serializer.data.get('new_password')

            if not check_password(old_password, user.password):
                return Response({'error': 'Invalid old password'}, status=status.HTTP_400_BAD_REQUEST)

            user.set_password(new_password)
            user.save()
            return Response({'message': 'Password changed successfully'}, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RequestPasswordResetEmailView(generics.GenericAPIView):
    serializer_class = RequestPasswordResetEmailSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        email = request.data["email"]

        if User.objects.filter(email=email).exists():
            user = User.objects.get(email=email)
            uidb64 = urlsafe_base64_encode(smart_bytes(user.id))
            token = PasswordResetTokenGenerator().make_token(user)
            current_site = get_current_site(request).domain
            relative_link = reverse(
                "Password-reset-confirm", kwargs={'uidb64': uidb64, 'token': token})
            absurl = 'http://'+current_site+relative_link
            email_body = f"Hello, \n Use link below to reset your password \n {absurl}"
            data = {'email_body': email_body, 'to_email': [user.email,],
                    'email_subject': 'Reset your password.'}

            # Send Message
            Utils.send_email(data)
        return Response({"Success": "We have send you a link to reset your password."}, status=status.HTTP_200_OK)


class PasswordTokenCheckAPIView(views.APIView):
    def get(self, request, uidb64, token):
        try:
            id = smart_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(id=id)
            print(user.__dict__)  # <User: username>
            if not PasswordResetTokenGenerator().check_token(user, token):
                return Response({"error": "Token is not valid, Please request a new one."}, status=status.HTTP_401_UNAUTHORIZED)
            return Response({"Success": True, "message": "Credentials valid", "uidb64": uidb64, "token": token}, status=status.HTTP_200_OK)
        except DjangoUnicodeDecodeError as identifier:
            return Response({"error": "Token is not valid, please request a new one."})


class SetNewPasswordAPIView(generics.GenericAPIView):
    serializer_class = SetNewPasswordSerializer

    def patch(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response({"Success": True, "message": "Password reset success."}, status=status.HTTP_200_OK)


class UserDetailsView(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = None

    def get_object(self):
        return self.request.user
