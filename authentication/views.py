from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .models import User, Profile
from .serializers import RegisterSerializer, CustomTokenRefreshSerializer, CustomTokenObtainPairSerializer, \
    ProfileSerializer


class Register(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer

    def perform_create(self, serializer):
        user = serializer.save()
        user.profile = Profile.objects.create(user=user)
        user.set_password(serializer.validated_data['password'])
        user.save()


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer


class CustomTokenRefreshView(TokenRefreshView):
    serializer_class = CustomTokenRefreshSerializer


class Me(generics.RetrieveUpdateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ProfileSerializer

    def get_object(self):
        return Profile.objects.get(user=self.request.user)
