from django.core.exceptions import ObjectDoesNotExist
from rest_framework import permissions
from . import JWTManager
from .models import User, Profile

jwt_manager = JWTManager.AuthHandler()

class IsSuperuserOrHR(permissions.IsAuthenticated):
    def has_permission(self, request, view):
        email = jwt_manager.get_user_from_auth_header(request)

        try:
            user = User.objects.get(email=email)
            profile = Profile.objects.get(user=user)

            if user.is_superuser or profile.job.title == 'HR':
                return True
            else:
                return False
        except ObjectDoesNotExist:
            return False


class IsSuperuserOrTD(permissions.IsAuthenticated):
    def has_permission(self, request, view):
        email = jwt_manager.get_user_from_auth_header(request)

        try:
            user = User.objects.get(email=email)
            profile = Profile.objects.get(user=user)

            if user.is_superuser or profile.job.title == 'TD':
                return True
            else:
                return False
        except ObjectDoesNotExist:
            return False

       