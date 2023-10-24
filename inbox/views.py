from rest_framework import generics
from .serializers import NewPositionSerializer
from .models import NewPositionModel


class NewPositionAPIView(generics.CreateAPIView):
    serializer_class = NewPositionSerializer
    queryset = NewPositionModel.objects.all()



