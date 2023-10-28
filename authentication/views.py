import jwt,uuid,redis,os
from loguru import logger
from django.conf import settings
from django.contrib.auth import authenticate
from django.core.mail import EmailMessage
from django.contrib.sites.shortcuts import get_current_site
from rest_framework import generics,authentication,views
from rest_framework.response import Response

from .models import User, Profile
from .serializers import RegisterSerializer, ProfileSerializer,LoginSerializer,RefreshTokenSerializer,OTPVerificationSerializer
from . import JWTManager

jwt_manager = JWTManager.AuthHandler()

LOG_FILE=os.path.abspath('logs/user.log')
log_dir = os.path.dirname(LOG_FILE)
if not os.path.exists(log_dir):
    os.makedirs(log_dir)

# Configure the logger
logger.add(LOG_FILE, rotation='500 MB', retention='7 days', level='INFO', format="{time:YYYY-MM-DD at HH:mm:ss} | {level} | {message}")
def generate_and_send_otp(email,current_site):
    otp = str(uuid.uuid4())
    r = redis.Redis(host='localhost', port=6379, db=0)
    
    r.setex(email, 100, otp)
    
    email_subject = 'Activate Account'
    email_message = f'Click the following link to activate your account:\n http://{current_site.domain}/auth/activate/{otp}'

    recipient_email = email
    
    EmailMessage(email_subject, email_message, settings.EMAIL_HOST_USER, [recipient_email]).send()



class Register(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer

    def perform_create(self, serializer):
        user = serializer.save()
        user.profile = Profile.objects.create(user=user)
        user.set_password(serializer.validated_data['password'])
        user.save()
        try:
            current_site = get_current_site(self.request)
            generate_and_send_otp(user.email,current_site) 
            logger.info(f'User account created: {user.email}')
        except Exception as e:
            return Response({'success': False, 'status': 400, 'error': e})




class VerifyAccount(views.APIView):
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
                    return Response({'success': True, 'status': 200, 'message': 'Account activated successfully'})
                else:
                    return Response({'success': False, 'status': 404, 'error': 'User not found for the provided email'})

        return Response({'success': False, 'status': 404, 'error': 'Invalid OTP'})


class Login(generics.CreateAPIView):
    serializer_class = LoginSerializer
    
    def create(self, request, *args, **kwargs):
        email = request.data.get('email')
        password = request.data.get('password')

        if not email or not password:
            return Response({'success': False, 'status': 400, 'error': 'Email and password are required'})
        
        user = authenticate(request, email=email, password=password)
        
        if user:
            logger.info(f'User {user.email} logged in successfully')
            login_token = jwt_manager.encode_login_token(user.email)
            message={
                'message':'You login successfuly',
                'data':login_token
            }
            return Response({'success': True, 'status': 200, 'message': message})
        else:
            return Response({'success': False, 'status': 401, 'error': 'Authentication failed'})
        


class Me(generics.RetrieveUpdateAPIView):
    authentication_classes = (authentication.TokenAuthentication, )
    serializer_class = ProfileSerializer

    def get_object(self):
        
        auth_header = self.request.META.get('HTTP_AUTHORIZATION') 

        if auth_header:
            auth_token = auth_header.split('Bearer ')[1] 
            user = jwt_manager.auth_access_wrapper(auth_token)

            if user:
                return Profile.objects.get(user__email=user)

class RefreshToken(generics.CreateAPIView):
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
        except (Exception) as exc : #TODO manage exceptions
            return Response({'success': False, 'status': 401, 'error': 'Invalid token'})
       

class Logout(generics.GenericAPIView):
    authentication_classes = (authentication.TokenAuthentication, )
    def get(self,request):
            user = request.user
            logger.info(f'User logged out: {user.email}')
            return Response({'success': True, 'status': 200, 'message': 'You logout successfuly'})


