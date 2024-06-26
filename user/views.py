from rest_framework import generics

from authentication.models import User
from authentication.permissions import IsSuperuserOrHR
from authentication.serializers import UserSerializer
from .models import Profile
from .serializers import ProfileSerializer


class UserListView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsSuperuserOrHR]


class ProfileAPIView(generics.RetrieveUpdateAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = [IsSuperuserOrHR]
    lookup_field = 'pk'
