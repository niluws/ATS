from rest_framework import serializers

from .models import CandidateModel, EducationModel, PreferencesModel, ExperiencesModel, AppointmentModel, SettingsModel, \
    InterviewSettingsModel, ScoreModel, InterviewerScore


class ExcelFileSerializer(serializers.Serializer):
    file = serializers.FileField()


class CandidateSerializer(serializers.ModelSerializer):
    status = serializers.CharField(source='statusmodel.status')

    class Meta:
        model = CandidateModel
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


class CandidateUpdateSerializer(serializers.ModelSerializer):
    resume = serializers.FileField(required=False)
    status = serializers.CharField(source='statusmodel.status', read_only=True)

    class Meta:
        model = CandidateModel
        fields = ['name', 'job', 'email', 'phone_number',
                  'province', 'location', 'marital', 'update_at',
                  'birthdate', 'gender', 'resume', 'candidate_approval', 'status',
                  'languages', 'skills', 'about']
        read_only_fields = ['name', 'job', 'email', 'phone_number',
                            'province', 'location', 'marital', 'update_at',
                            'birthdate', 'gender', 'status']


class PDFScoreSerializer(serializers.ModelSerializer):
    candidate = CandidateSerializer(read_only=True)

    class Meta:
        model = ScoreModel
        fields = ['id', 'candidate', 'auto_score', 'pdf_score']
        read_only_fields = ['id', 'candidate', 'auto_score']

    def update(self, instance, validated_data):
        instance.pdf_score = validated_data.get('pdf_score', instance.pdf_score)
        instance.save()
        return instance


class AppointmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = AppointmentModel
        fields = '__all__'


class SettingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = SettingsModel
        fields = '__all__'


class InterviewSettingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = InterviewSettingsModel
        fields = '__all__'


class InterviewerScoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = InterviewerScore
        fields = ['interviewer', 'question', 'score']
        read_only_fields = ['interviewer']
