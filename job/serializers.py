from rest_framework import serializers
from .models import Job
from authentication.models import Profile

class JobSerializer(serializers.ModelSerializer):
    class Meta:
        model = Job
        fields = '__all__'

