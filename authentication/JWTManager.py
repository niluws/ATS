import jwt
from datetime import datetime, timedelta
from rest_framework.response import Response


class AuthHandler:
    SECRET_KEY = "e850730693d632d699dedab3ced649a8badad345dae49c20ab9989622b840868"
    ALGORITHM = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES = 180
    REFRESH_TOKEN_EXPIRE_MINUTES = 1440
    
    
    def encode_token(self, data):
        
        payload = dict(
			iss = data,
		)
        to_encode = payload.copy()
       
        to_encode.update({"exp": datetime.utcnow() + timedelta(minutes=self.ACCESS_TOKEN_EXPIRE_MINUTES)})
        to_encode.update({'exp': datetime.utcnow()+ timedelta(minutes=self.REFRESH_TOKEN_EXPIRE_MINUTES)})
        return jwt.encode(to_encode,self.SECRET_KEY,algorithm=self.ALGORITHM)
    
    def encode_login_token(self, data:dict):
        access_token=self.encode_token(data)
        refresh_token=self.encode_token(data)

        login_token = dict(
			access_token=f"{access_token}",
			refresh_token=f"{refresh_token}"
		) 
        
        return login_token
    
    def encode_update_token(self, username):
        access_token = self.encode_token(username, "access_token")

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
            return Response({'success': False, 'status': 401, 'error': 'Sinature has expired'})

        except jwt.InvalidTokenError as e:
            return Response({'success': False, 'status': 401, 'error': 'Invalid token'})

        
    def auth_access_wrapper(self, token):
        return self.decode_access_token(token)

    def auth_refresh_wrapper(self, token):
        return self.decode_refresh_token(token)
