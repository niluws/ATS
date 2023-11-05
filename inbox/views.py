from rest_framework import generics,viewsets
from .serializers import BasePositionSerializer,HRApprovalSerializer,TDApprovalSerializer
from .models import NewPositionModel
from authentication.permissions import IsSuperuserOrHR,IsSuperuserOrTD

class NewPositionViewSet(viewsets.ModelViewSet):
    serializer_class = BasePositionSerializer
    queryset = NewPositionModel.objects.all()


class HRApproval(generics.RetrieveUpdateAPIView):
    serializer_class = HRApprovalSerializer
    queryset = NewPositionModel.objects.all()
    permission_classes=[IsSuperuserOrHR]


class TDApproval(generics.RetrieveUpdateAPIView):
    serializer_class = TDApprovalSerializer
    queryset=NewPositionModel.objects.all()
    permission_classes=[IsSuperuserOrTD]
