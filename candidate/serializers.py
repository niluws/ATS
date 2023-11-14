from rest_framework import serializers
from .models import ExcelFileModel,CandidateModel,EducationModel,PreferencesModel

class ExcelFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExcelFileModel
        fields = ['file']

class CandidateSerializer(serializers.ModelSerializer):
    class Meta:
        model=CandidateModel
        fields='__all__'

class EducationModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = EducationModel
        fields = '__all__'


class EducationModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = EducationModel
        fields = '__all__'

class PreferencesModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = PreferencesModel
        fields = '__all__'

class ScoreSerializer(serializers.ModelSerializer):
    education = EducationModelSerializer(source='educationmodel_set', many=True, read_only=True)
    preferences = PreferencesModelSerializer(source='preferencesmodel', read_only=True)

    class Meta:
        model = CandidateModel
        fields = '__all__'
