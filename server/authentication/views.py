from rest_framework import generics, status
from .models import User
from .serializers import RegisterSerializer
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

# Create your views here.


class RegisterView(generics.GenericAPIView):
    serializer_class = RegisterSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        user = User.objects.get(email=serializer.data['email'])
        token = RefreshToken.for_user(user).access_token
        return Response(serializer.data, status=status.HTTP_201_CREATED)
