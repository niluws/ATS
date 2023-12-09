from datetime import datetime, timedelta

import jwt
from rest_framework import authentication
from rest_framework.exceptions import AuthenticationFailed


class AuthHandler(authentication.BaseAuthentication):
    SECRET_KEY = "e850730693d632d699dedab3ced649a8badad345dae49c20ab9989622b840868"
    ALGORITHM = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES = 100
    REFRESH_TOKEN_EXPIRE_MINUTES = 60 * 30

    def encode_token(self, data, expire_minutes):
        payload = dict(iss=data)
        to_encode = payload.copy()
        to_encode.update({"exp": datetime.utcnow() + timedelta(minutes=expire_minutes)})
        return jwt.encode(to_encode, self.SECRET_KEY, algorithm=self.ALGORITHM)

    def encode_login_token(self, data: dict):
        access_token = self.encode_token(data, self.ACCESS_TOKEN_EXPIRE_MINUTES)
        refresh_token = self.encode_token(data, self.REFRESH_TOKEN_EXPIRE_MINUTES)

        login_token = dict(
            access_token=f"{access_token}",
            refresh_token=f"{refresh_token}"
        )

        return login_token

    def decode_access_token(self, token):
        try:
            payload = jwt.decode(token, self.SECRET_KEY, algorithms=self.ALGORITHM)
            return payload['iss']
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed(detail='Token has expired', code=401)
        except jwt.InvalidTokenError:
            raise AuthenticationFailed(detail='Token is invalid', code=401)

    def decode_refresh_token(self, token):
        try:
            payload = jwt.decode(token, self.SECRET_KEY, algorithms=self.ALGORITHM)
            return payload['iss']
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed(detail='Token has expired', code=401)
        except jwt.InvalidTokenError:
            raise AuthenticationFailed(detail='Token is invalid', code=401)

    def auth_refresh_wrapper(self, token):
        return self.decode_refresh_token(token)

    def get_user_from_auth_header(self, request):
        auth_header = request.META.get('HTTP_AUTHORIZATION')
        if auth_header:
            return self.decode_access_token(auth_header)
        else:
            raise AuthenticationFailed(detail='No token found,please authenticate', code=401)
