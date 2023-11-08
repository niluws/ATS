from rest_framework import viewsets,generics
from authentication.permissions import IsSuperuserOrHR,IsSuperuserOrTD
from .serializers import JobSerializer, BasePositionSerializer,HRApprovalSerializer,TDApprovalSerializer,JobRequirementSerializer
from .models import Job,NewPositionModel,JobRequirement

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

class JobRequirementViewSet(viewsets.ModelViewSet):
    queryset = JobRequirement.objects.all()
    serializer_class = JobRequirementSerializer
    permission_classes=[IsSuperuserOrTD]
