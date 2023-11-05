from rest_framework import viewsets
from .serializers import JobSerializer
from .models import Job
from authentication.permissions import IsSuperuserOrHR
class JobViewSet(viewsets.ModelViewSet):
    serializer_class = JobSerializer
    queryset = Job.objects.all() 
    permission_classes=[IsSuperuserOrHR]

