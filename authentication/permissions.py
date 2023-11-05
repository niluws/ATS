from rest_framework import permissions
from . import JWTManager
from .models import User, Profile

jwt_manager = JWTManager.AuthHandler()

class IsSuperuserOrHR(permissions.IsAuthenticated):
    def has_permission(self, request, view):
        email = jwt_manager.get_user_from_auth_header(request)
        user=User.objects.get(email=email)
        
        if email:
            profile=Profile.objects.get(user=user)
            if user.is_superuser or profile.job.title == 'HR':
                print('true')
                return True
            else:return False


class IsSuperuserOrTD(permissions.IsAuthenticated):
    def has_permission(self, request, view):
        email = jwt_manager.get_user_from_auth_header(request)
        user=User.objects.get(email=email)
        
        if email:
            profile=Profile.objects.get(user=user)
            if user.is_superuser or profile.job.title == 'TD':
                print('true')
                return True
            else:return False 

       