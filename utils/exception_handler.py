from rest_framework.response import Response


def exception_handler(func):
    def wrapper(*args, **kwargs):
        try:
            result = func(*args, **kwargs)
            return result
        except Exception as e:
            print(f"Exception caught in {func.__name__}: {str(e)}")
            return Response({'success': False, 'error': f"Exception caught in {func.__name__}: {str(e)}"})
    return wrapper