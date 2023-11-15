import jwt,uuid,redis,logging
from functools import wraps
from datetime import datetime
import logging.config
from django.core.mail import EmailMessage
from django.contrib.sites.shortcuts import get_current_site
from rest_framework import generics,views,permissions
from rest_framework.response import Response

from utils import config
from .models import User
from user.models import Profile
from .serializers import RegisterSerializer,LoginSerializer,RefreshTokenSerializer,LogoutSerializer
from user.serializers import ProfileSerializer
from . import JWTManager




jwt_manager = JWTManager.AuthHandler()

def log_user_activity(func):

    @wraps(func)
    def wrapper_func(self, request, *args, **kwargs):

        response=func(self, request, *args, **kwargs)
        print(request.data)
        logger = logging.getLogger('user_activity')
        user = request.data.get('user_id')
        message = request.data.get('message')
        asctime=datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')
        logger.info(f'{asctime} - INFO - user_id: {user} {message}')
     
        return response

    return wrapper_func


def generate_and_send_otp(email,current_site):
    otp = str(uuid.uuid4())
    r = redis.Redis(host='localhost', port=6379, db=0)
    
    r.set(email, otp,ex=500)
    
    email_subject = 'Activate Account'
    email_message = f'Click the following link to activate your account:\n http://{current_site.domain}/auth/activate/{otp}'

    recipient_email = email
    
    EmailMessage(email_subject, email_message, config.EMAIL_HOST_USER, [recipient_email]).send()



class RegisterAPIView(generics.CreateAPIView):
    serializer_class = RegisterSerializer

    
    def perform_create(self, serializer):
        
        
        try:
            user = serializer.save()
            user.profile = Profile.objects.create(user=user)
            user.set_password(serializer.validated_data['password'])
            user.save()
            self.request.data['message'] ='registered'
            self.request.data['user_id'] =user.pk

            current_site = get_current_site(self.request)
            generate_and_send_otp(user.email,current_site) 
        except Exception as e:
            return Response({'success': False, 'status': 400, 'error': e})
        
    @log_user_activity
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)



class VerifyAccountAPIView(views.APIView):
    def get(self, request, otp_code):
        r = redis.Redis(host='localhost', port=6379, db=0)

        keys = r.keys('*')

        for key in keys:
            value = r.get(key)

            if value.decode('utf-8') == otp_code:
                user = User.objects.filter(email=key.decode('utf-8')).first()

                if user:
                    user.is_active = True
                    user.save()
                    r.delete(key)
                    return Response({'success': True, 'status': 200, 'message': 'Account activated successfully'})
                else:
                    return Response({'success': False, 'status': 404, 'error': 'User not found for the provided email'})

        return Response({'success': False, 'status': 404, 'error': 'Invalid OTP'})


class LoginAPIView(generics.CreateAPIView):
    serializer_class = LoginSerializer
    permission_classes=[permissions.AllowAny]
        
    @log_user_activity
    def create(self, request, *args, **kwargs):
        email = request.data.get('email')
        password = request.data.get('password')
        user=User.objects.filter(email=email).first()

        if not email or not password:
            return Response({'success': False, 'status': 400, 'error': 'Email and password are required'})
        if user.is_active:

            if user:
                login_token = jwt_manager.encode_login_token(user.email)
                request.data['user_id'] = user.pk
                request.data['message'] = 'looged in'
                
                message={
                    'message':'You login successfuly',
                    'data':login_token,
                    
                }
                return Response({'success': True, 'status': 200, 'message': message})
            else:
                return Response({'success': False, 'status': 401, 'error': 'Authentication failed'})
        else:return Response({'success': False, 'status': 401, 'error': 'Chack your email and verify your account'})



class MeAPIView(generics.RetrieveUpdateAPIView):
    serializer_class = ProfileSerializer
    def get_object(self):
        user = jwt_manager.get_user_from_auth_header(self.request)
        profile=Profile.objects.get(user__email=user)
        return profile
    
    def get(self, request, *args, **kwargs):
        
        user = jwt_manager.get_user_from_auth_header(self.request)
        if user:
            profile=Profile.objects.get(user__email=user)
            profile=ProfileSerializer(profile).data
            return Response(profile)
        else:
            return Response({'success': False, 'status': 401, 'error': 'User is not authenticated'})


class RefreshTokenAPIView(generics.CreateAPIView):
    serializer_class=RefreshTokenSerializer

    def create(self, request):
        refresh_token = request.data.get('refresh_token')

        if not refresh_token:
            return Response({'success': False, 'status': 400, 'error': 'Refresh token is required'})
      
        try:
            email = jwt_manager.auth_refresh_wrapper(refresh_token)

            if email:
                login_token = jwt_manager.encode_login_token(email)
                return Response({'success': True, 'status': 200, 'message': login_token})
            else:
                return Response({'success': False, 'status': 401, 'error': 'You are not authorized'})
        except jwt.ExpiredSignatureError:
            return Response({'success': False, 'status': 401, 'error': 'Signature has expired'})
        except Exception :
            return Response({'success': False, 'status': 401, 'error': 'Invalid token'})
       

class LogoutAPIView(generics.GenericAPIView):
    serializer_class = LogoutSerializer

    @log_user_activity
    def get(self,request):
            auth =jwt_manager.get_user_from_auth_header(self.request)
            user = User.objects.get(email=auth)
 
            if auth:
                request.data['user_id'] = user.id
                request.data['message'] = 'logged out'
        
                return Response({'success': True, 'status': 200, 'message': 'You logout successfuly'})
            else:
                return Response({'success': False, 'status': 401, 'error': 'User is not authenticated'})


