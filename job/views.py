from rest_framework import viewsets,generics
from .serializers import JobSerializer, BasePositionSerializer,HRApprovalSerializer,TDApprovalSerializer
from .models import Job
from authentication.permissions import IsSuperuserOrHR
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

class JobViewSet(viewsets.ModelViewSet):
    serializer_class = JobSerializer
    queryset = Job.objects.all() 
    permission_classes=[IsSuperuserOrHR]

