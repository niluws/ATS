from functools import wraps

from rest_framework.response import Response

from authentication.models import LogExceptionModel, LogUserModel


def log_user_activity(func):
    @wraps(func)
    def wrapper_func(self, request, *args, **kwargs):
        response = func(self, request, *args, **kwargs)

        if response and type(response) is str and ('log' in response.data or 'error' in response.data):
            log = response.data.get("log")
            error = response.data.get("error")
            if log:
                user_id = log.get("user_id")
                event = log.get("event")
                LogUserModel.objects.create(event=event, user_id=user_id)
            elif error:
                LogExceptionModel.objects.create(error=error)
        return response

    return wrapper_func


def exception_handler(func):
    @log_user_activity
    def wrapper(*args, **kwargs):
        try:
            result = func(*args, **kwargs)
            return result
        except Exception as e:
            return Response({'success': False, 'error': str(e)})

    return wrapper
