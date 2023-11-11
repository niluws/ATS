from rest_framework import serializers
from .models import ExcelFileModel,CandidateModel

class ExcelFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExcelFileModel
        fields = ['file']

class CandidateSerializer(serializers.ModelSerializer):
    class Meta:
        model=CandidateModel
        fields='__all__'