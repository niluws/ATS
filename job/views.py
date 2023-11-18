from rest_framework import viewsets,generics
from rest_framework.response import Response
from authentication.permissions import IsSuperuserOrHR,IsSuperuserOrTD,IsAuthenticated
from .serializers import JobSerializer, BasePositionSerializer,HRApprovalSerializer,TDApprovalSerializer,JobRequirementSerializer
from .models import Job,NewPositionModel,JobRequirement

class NewPositionViewSet(viewsets.ModelViewSet):
    serializer_class = BasePositionSerializer
    queryset = NewPositionModel.objects.all()
    permission_classes=[IsAuthenticated]


class HRApproval(generics.RetrieveUpdateAPIView):
    serializer_class = HRApprovalSerializer
    queryset = NewPositionModel.objects.all()
    permission_classes=[IsSuperuserOrHR]


class TDApproval(generics.RetrieveUpdateAPIView):
    serializer_class = TDApprovalSerializer
    queryset=NewPositionModel.objects.all()
    permission_classes=[IsSuperuserOrTD]

    def put(self, request, *args, **kwargs):
        instance = self.get_object()
        if not instance.hr_approval:
            return Response({"error": "HR approval is required to update this data."},status=403)
        if instance.td_approval is False and 'interviewer' not in request.data:
            return Response({"error": "The 'interviewer' field is required.You should add interviewer"},status=400)
        

        serializer = self.get_serializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        return Response(serializer.data)

class JobViewSet(viewsets.ModelViewSet):
    serializer_class = JobSerializer
    queryset = Job.objects.all() 
    permission_classes=[IsSuperuserOrHR]

class JobRequirementViewSet(viewsets.ModelViewSet):
    queryset = JobRequirement.objects.all()
    serializer_class = JobRequirementSerializer
    permission_classes=[IsSuperuserOrTD]
