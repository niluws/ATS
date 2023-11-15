import jwt
from datetime import datetime, timedelta
from rest_framework.response import Response

class AuthHandler:
    SECRET_KEY = "e850730693d632d699dedab3ced649a8badad345dae49c20ab9989622b840868"
    ALGORITHM = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES = 7
    REFRESH_TOKEN_EXPIRE_MINUTES = 7

    def encode_token(self, data, expire_minutes):
        payload = dict(iss=data)
        to_encode = payload.copy()
        to_encode.update({"exp": datetime.utcnow() + timedelta(days=expire_minutes)})
        return jwt.encode(to_encode, self.SECRET_KEY, algorithm=self.ALGORITHM)

    def encode_login_token(self, data: dict):
        access_token = self.encode_token(data, self.ACCESS_TOKEN_EXPIRE_MINUTES).decode('utf-8')
        refresh_token = self.encode_token(data, self.REFRESH_TOKEN_EXPIRE_MINUTES).decode('utf-8')

        login_token = dict(
            access_token=f"{access_token}",
            refresh_token=f"{refresh_token}"
        )

        return login_token

    def encode_update_token(self, username):
        access_token = self.encode_token(username, self.ACCESS_TOKEN_EXPIRE_MINUTES).decode('utf-8')

        update_token = dict(
            access_token=f"{access_token}"
        )
        return update_token

    def decode_access_token(self, token):
        try:
            payload = jwt.decode(token, self.SECRET_KEY, algorithms=self.ALGORITHM)
            return payload['iss']
        except jwt.ExpiredSignatureError:
            return Response({'success': False, 'status': 401, 'error': 'Signature has expired'})

        except jwt.InvalidTokenError as e:
            return Response({'success': False, 'status': 401, 'error': 'Invalid token'})

    def decode_refresh_token(self, token):
        try:
            payload = jwt.decode(token, self.SECRET_KEY, algorithms=self.ALGORITHM)
            return payload['iss']
        except jwt.ExpiredSignatureError:
            return Response({'success': False, 'status': 401, 'error': 'Signature has expired'})

        except jwt.InvalidTokenError as e:
            return Response({'success': False, 'status': 401, 'error': 'Invalid token'})

    def auth_access_wrapper(self, token):
        return self.decode_access_token(token)

    def auth_refresh_wrapper(self, token):
        return self.decode_refresh_token(token)

    def get_user_from_auth_header(self, request):
        auth_header = request.META.get('HTTP_AUTHORIZATION')

        if auth_header:
            return self.auth_access_wrapper(auth_header)
