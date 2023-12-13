from django.db.models import Count
from rest_framework import views
from rest_framework.response import Response

from .serializers import StatusModelSerializer
from candidate.models import StatusModel, CandidateModel
from utils import exception_handler

exception_handler = exception_handler.exception_handler


class CandidateStatusAPIView(views.APIView):

    @exception_handler
    def get(self, request):
        waiting_for_interview = StatusModel.objects.filter(status='WI').count()
        approved = StatusModel.objects.filter(status='A').count()
        rejected = StatusModel.objects.filter(status='R').count()
        hired = StatusModel.objects.filter(status='H').count()

        queryset = StatusModel.objects.all()
        serializer = StatusModelSerializer(queryset, many=True)

        message = {
            'data': serializer.data,
            'waiting_for_interview': waiting_for_interview,
            'Approved': approved,
            'Rejected': rejected,
            'Hired': hired,

        }
        return Response({'success': True, 'status': 200, 'message': message})


class CandidateJobStatisticAPIView(views.APIView):

    @exception_handler
    def get(self, request):
        statistic = (
            CandidateModel.objects.values('job').annotate(candidate_count=Count('id')).order_by('job')
        )

        result = {item['job']: item['candidate_count'] for item in statistic}

        return Response({'success': True, 'status': 200, 'message': result})
