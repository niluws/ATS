from django.core.exceptions import ObjectDoesNotExist
from rest_framework import permissions
from rest_framework.exceptions import AuthenticationFailed
from . import JWTManager
from .models import User
from user.models import Profile

jwt_manager = JWTManager.AuthHandler()

class IsSuperuserOrHR(permissions.IsAuthenticated):
    def has_permission(self, request, view):
        email = jwt_manager.get_user_from_auth_header(request)

        try:
            user = User.objects.get(email=email)
            profile = Profile.objects.get(user=user)

            if user.is_superuser or profile.job.title == 'HR':
                return True

        except :
            raise AuthenticationFailed(detail='You are not HR or admin', code=401)

class IsSuperuserOrTD(permissions.IsAuthenticated):
    def has_permission(self, request, view):
        email = jwt_manager.get_user_from_auth_header(request)

        try:
            user = User.objects.get(email=email)
            profile = Profile.objects.get(user=user)

            if user.is_superuser or profile.role.title == 'TD':
                return True

        except :
            raise AuthenticationFailed(detail='You are not TD or admin', code=401)


class IsAuthenticated(permissions.IsAuthenticated):
    def has_permission(self, request, view):
        email = jwt_manager.get_user_from_auth_header(request)

        try:
            user = User.objects.get(email=email)
            profile = Profile.objects.get(user=user)

            if profile:
                return True

        except :raise AuthenticationFailed(detail='You have no profile', code=401)

