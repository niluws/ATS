from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer, TokenRefreshSerializer
from rest_framework_simplejwt.tokens import RefreshToken, TokenError
from .models import User, Profile


class RegisterSerializer(serializers.ModelSerializer):
    confirm_password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'password', 'confirm_password']

    def validate(self, attrs):
        if attrs['password'] != attrs['confirm_password']:
            raise serializers.ValidationError({"confirm_password": "Password fields didn't match."})
        attrs.pop('confirm_password')
        return attrs


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    username_field = 'email'


class CustomTokenRefreshSerializer(TokenRefreshSerializer):
    username_field = 'email'


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = '__all__'


class LogoutSerializer(serializers.Serializer):
    refresh = serializers.CharField()

    def validate(self, attr):
        self.token = attr['refresh']
        return attr

    def save(self, **kwargs):
        try:
            RefreshToken(self.token).blacklist()
        except TokenError:
            self.fail('bad token')
