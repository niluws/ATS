from rest_framework import generics
from .serializers import BasePositionSerializer,HRApprovalSerializer,TDApprovalSerializer
from .models import NewPositionModel

#implement permitions

class NewPositionAPIView(generics.CreateAPIView):
    serializer_class = BasePositionSerializer
    queryset = NewPositionModel.objects.all()


class HRApproval(generics.RetrieveUpdateAPIView):
    serializer_class = HRApprovalSerializer
    queryset = NewPositionModel.objects.all()


class TDApproval(generics.RetrieveUpdateAPIView):
    serializer_class = TDApprovalSerializer
    queryset=NewPositionModel.objects.all()
