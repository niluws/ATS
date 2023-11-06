from rest_framework import serializers
from .models import ExceFileModel

class ExcelFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExceFileModel
        fields = ['file']
