from rest_framework import viewsets, generics, parsers, views
from rest_framework.response import Response

from authentication.models import User
from authentication.permissions import IsSuperuserOrTD
from .models import Job, NewPositionModel, JobRequirement, QuestionsModel
from .serializers import JobSerializer, BasePositionSerializer, HRApprovalSerializer, TDApprovalSerializer, \
    JobRequirementSerializer, QuestionsSerializer


class NewPositionViewSet(viewsets.ModelViewSet):
    serializer_class = BasePositionSerializer
    queryset = NewPositionModel.objects.all()
    # permission_classes = [IsAuthenticated]
    parser_classes = (parsers.MultiPartParser,)


class HRApproval(generics.RetrieveUpdateAPIView):
    serializer_class = HRApprovalSerializer
    queryset = NewPositionModel.objects.all()
    # permission_classes = [IsSuperuserOrHR]
    parser_classes = (parsers.MultiPartParser,)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        td_user = User.objects.filter(profile__role__title='TD',
                                      profile__department=serializer.data.get('department')).first()
        if td_user is None:
            return Response({'status': 400, 'error': 'No TD user exists for the specified department'})

        if getattr(instance, '_prefetched_objects_cache', None):
            instance._prefetched_objects_cache = {}

        return Response(serializer.data)


class TDApproval(generics.RetrieveUpdateAPIView):
    serializer_class = TDApprovalSerializer
    queryset = NewPositionModel.objects.all()
    permission_classes = [IsSuperuserOrTD]

    def put(self, request, *args, **kwargs):
        instance = self.get_object()
        if not instance.hr_approval:
            return Response({"error": "HR approval is required for update this data.Wait for HR approval"}, status=403)
        if instance.td_approval is False and 'interviewer' not in request.data:
            return Response({"error": "The 'interviewer' field is required.You should add interviewer"}, status=400)

        serializer = self.get_serializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        return Response(serializer.data)


class JobViewSet(viewsets.ModelViewSet):
    serializer_class = JobSerializer
    queryset = Job.objects.all()
    # permission_classes = [IsSuperuserOrHR]


class JobRequirementViewSet(viewsets.ModelViewSet):
    queryset = JobRequirement.objects.all()
    serializer_class = JobRequirementSerializer
    # permission_classes = [IsSuperuserOrTD]


class QuestionsViewSet(viewsets.ModelViewSet):
    queryset = QuestionsModel.objects.all()
    serializer_class = QuestionsSerializer


