from rest_framework import serializers
from .models import ExceFileModel,CandidateModel

class ExcelFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExceFileModel
        fields = ['file']

class CandidateSerializer(serializers.ModelSerializer):
    class Meta:
        model=CandidateModel
        fields='__all__'