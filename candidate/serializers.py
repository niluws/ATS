from rest_framework import serializers
from .models import CandidateModel,EducationModel,PreferencesModel,ExperiencesModel,AppointmentModel

class ExcelFileSerializer(serializers.Serializer):
    file=serializers.FileField()

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

class ExperiencesModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExperiencesModel
        fields = '__all__'

class ScoreSerializer(serializers.ModelSerializer):
    education = EducationModelSerializer(source='educationmodel_set', many=True, read_only=True)
    preferences = PreferencesModelSerializer(source='preferencesmodel', read_only=True)
    experiences = ExperiencesModelSerializer(source='experiencesmodel_set',read_only=True,many=True,)

    class Meta:
        model = CandidateModel
        fields = '__all__'

class CandidateUpdateSerializer(serializers.ModelSerializer):

    class Meta:
        model = CandidateModel
        fields = ['name', 'job', 'email', 'phone_number',
                   'province', 'location', 'marital','update_at',
                    'birthdate', 'gender','resume','invitation_count']
        read_only_fields = ['name', 'job', 'email', 'phone_number',
                   'province', 'location', 'marital','update_at',
                    'birthdate', 'gender','invitation_count']


class AppointmentSerializer(serializers.ModelSerializer):
    # interview_time_jalali = serializers.ReadOnlyField(source='interview_time_jalali')
    candidate=serializers.StringRelatedField()
    class Meta:
        model = AppointmentModel
        fields = '__all__'