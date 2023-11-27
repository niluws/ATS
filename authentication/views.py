import logging
import logging.config
import redis
import uuid
from datetime import datetime
from functools import wraps

from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from rest_framework import generics, views, permissions
from rest_framework.response import Response

from user.models import Profile
from utils import config
from . import JWTManager
from .models import User
from .serializers import RegisterSerializer, LoginSerializer, RefreshTokenSerializer, LogoutSerializer, MeSerializer,VerifyEmailSerializer

jwt_manager = JWTManager.AuthHandler()


def log_user_activity(func):
    @wraps(func)
    def wrapper_func(self, request, *args, **kwargs):
        response = func(self, request, *args, **kwargs)
        logger = logging.getLogger("user_activity")
        user = dict(response.data).get("message").get("user_id")
        message = dict(response.data).get("message").get("message")
        asctime = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
        logger.info(f"{asctime} - INFO - user_id: {user}, {message} ")

        return response

    return wrapper_func


def generate_and_send_otp(email, current_site):
    try:
        otp = str(uuid.uuid4())
        r = redis.Redis(host='localhost', port=6379, db=0)

        r.set(email, otp, ex=500)

        email_subject = 'Activate Account'
        email_message = f'Click the following link to activate your account:\n' \
                        f' http://{current_site.domain}/auth/activate/{otp}'

        recipient_email = email

        EmailMessage(email_subject, email_message, config.EMAIL_HOST_USER, [recipient_email]).send()
    except:
        return Response({'success': False, 'status': 400, 'error': 'You should active redis at first'})


class RegisterAPIView(generics.CreateAPIView):
    serializer_class = RegisterSerializer

    @log_user_activity
    def post(self, request, *args, **kwargs):
        try:

            serializer = self.get_serializer(data=request.data)
            email = request.data.get('email')
            password = request.data.get('password')
            confirm_password = request.data.get('confirm_password')
            user = User.objects.filter(email=email).first()

            if user:
                return Response({'success': False, 'status': 400,
                                 'error': 'Email already exists. Please choose a different email address'})
            elif password != confirm_password:
                return Response({'success': False, 'status': 400, 'error': 'Password fields are not match'})
            serializer.is_valid(raise_exception=True)
            user = serializer.save()
            user.set_password(serializer.validated_data['password'])
            user.save()

            message = {
                'user_id': user.pk,
                'message': 'Registered successfully',
                'first_name': serializer.validated_data.get('first_name'),
                'last_name': serializer.validated_data.get('last_name'),
                'email': email,
            }

            return Response({'success': True, 'status': 201, 'message': message})
        except Exception as e:
            return Response({'success': False, 'status': 400, 'error': str(e)})


class LoginAPIView(generics.CreateAPIView):
    serializer_class = LoginSerializer

    @log_user_activity
    def create(self, request, *args, **kwargs):
        email = request.data.get('email')
        password = request.data.get('password')
        user = User.objects.filter(email=email).first()

        if not email or not password:
            return Response({'success': False, 'status': 400, 'error': 'Email and password are required'})

        if user:
            if user.is_active:
                if not user.check_password(password):
                    return Response({'success': False, 'status': 401, 'error': 'Incorrect password'})
                login_token = jwt_manager.encode_login_token(user.email)

                message = {
                    'message': 'Logged in successfully',
                    'data': login_token,
                    'user_id': user.pk,
                }
                return Response({'success': True, 'status': 200, 'message': message})
            else:
                return Response({'success': False, 'status': 401, 'error': 'Chack your email and verify your account'})
        else:
            return Response({'success': False, 'status': 401, 'error': 'Email not found. Check your email'})


class LogoutAPIView(generics.GenericAPIView):
    serializer_class = LogoutSerializer

    @log_user_activity
    def get(self, request):
        auth = jwt_manager.get_user_from_auth_header(self.request)
        user = User.objects.get(email=auth)
        if auth:
            message = {
                'message': 'Logout successfully',
                'user_id': user.pk,
            }

            return Response({'success': True, 'status': 200, 'message': message})
        else:
            return Response({'success': False, 'status': 401, 'error': 'User is not authenticated'})


class MeAPIView(generics.RetrieveUpdateAPIView):
    serializer_class = MeSerializer

    def get_object(self):
        user = jwt_manager.get_user_from_auth_header(self.request)

        user = User.objects.get(email__iexact=user)
        return user

    def get(self, request, *args, **kwargs):
        user = jwt_manager.get_user_from_auth_header(self.request)
        if user:
            try:
                user = User.objects.get(email__iexact=user)
                user = MeSerializer(user).data
                return Response(user)

            except:
                return Response({'success': False, 'status': 401, 'error': 'You have no profile'})


class RefreshTokenAPIView(generics.CreateAPIView):
    serializer_class = RefreshTokenSerializer

    def create(self, request):
        refresh_token = request.data.get('refresh_token')

        if not refresh_token:
            return Response({'success': False, 'status': 400, 'error': 'Refresh token is required'})

        email = jwt_manager.auth_refresh_wrapper(refresh_token)
        if email:
            login_token = jwt_manager.encode_login_token(email)
            return Response({'success': True, 'status': 200, 'message': login_token})
        else:
            return Response({'success': False, 'status': 401, 'error': 'You are not authorized'})


class VerifyAccountAPIView(views.APIView):
    def get(self, request, otp_code):

        r = redis.Redis(host='localhost', port=6379, db=0)
        keys = r.keys('*')

        for key in keys:

            value = r.get(key)

            if value.decode('utf-8') == otp_code:
                user = User.objects.filter(email=key.decode('utf-8')).first()
                user.is_active = True
                user.save()
                r.delete(key)

                return Response({'success': True, 'status': 200, 'message': 'Account activated successfully'})

        return Response({'success': False, 'status': 404, 'error': 'Invalid OTP code'})


class VerifyEmailAPIView(generics.CreateAPIView):
    serializer_class = VerifyEmailSerializer

    def post(self, request, *args, **kwargs):
        email = request.data['email']
        user=User.objects.filter(email=email).first()

        if user:
            if  user.is_active is False:
                current_site = get_current_site(self.request)
                generate_and_send_otp(email, current_site)
                return Response({'success': True, 'status': 200, 'message': 'Email sent successfully.'})
            
            else:return Response({'success': True, 'status': 400, 'message': 'Your account is already activate'})

        else:return Response({'success': True, 'status': 400, 'message': 'Email not found.please register first'})
