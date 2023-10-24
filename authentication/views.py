from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.urls import reverse
from rest_framework import generics
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from .models import User, Profile
from .serializers import RegisterSerializer, CustomTokenRefreshSerializer, CustomTokenObtainPairSerializer, \
    ProfileSerializer, LogoutSerializer


class Register(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer

    def perform_create(self, serializer):
        user = serializer.save()
        user.profile = Profile.objects.create(user=user)
        user.set_password(serializer.validated_data['password'])
        user.save()
        current_site = get_current_site(self.request)
        activation_url = reverse('activate_account', args=[str(user.active_code)])
        activation_url = f'http://{current_site.domain}{activation_url}'
        email_subject = 'Activation Code'
        email_message = f'Click the following link to activate your account:\n{activation_url}'
        sender_email = settings.EMAIL_HOST_USER
        recipient_email = user.email
        EmailMessage(email_subject, email_message, sender_email, [recipient_email]).send()


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer


class CustomTokenRefreshView(TokenRefreshView):
    serializer_class = CustomTokenRefreshSerializer


class Me(generics.RetrieveUpdateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ProfileSerializer

    def get_object(self):
        return Profile.objects.get(user=self.request.user)


class Logout(generics.GenericAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = LogoutSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)


def activate_account(request, active_code):
    User = get_user_model()
    user = get_object_or_404(User, active_code=active_code)

    user.is_active = True
    user.save()

    return JsonResponse({"message": "Your account is now activated."})
