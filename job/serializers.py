from rest_framework import serializers

from .models import Job, NewRequestModel, Requirement, JobRequirement, QuestionsModel, Role


class BaseNewRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = NewRequestModel
        fields = ['id', 'position_title', 'contract_type', 'reason', 'education_level', 'experience_level',
                  'department', 'quantity', 'budget', 'status']
        read_only_fields = ['status']


class HRApprovalSerializer(BaseNewRequestSerializer):
    class Meta(BaseNewRequestSerializer.Meta):
        fields = BaseNewRequestSerializer.Meta.fields + ['hr_approval', 'assigned_to_td', 'is_advertised', 'message']
        read_only_fields = BaseNewRequestSerializer.Meta.fields + ['assigned_to_td']


class TDApprovalSerializer(HRApprovalSerializer):
    class Meta(HRApprovalSerializer.Meta):
        fields = HRApprovalSerializer.Meta.fields + ['interviewer', 'td_approval']
        read_only_fields = HRApprovalSerializer.Meta.fields

    def update(self, instance, validated_data):
        if not validated_data.get('td_approval', instance.td_approval):
            validated_data.pop('interviewer')

        return super().update(instance, validated_data)


class QuestionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuestionsModel
        fields = '__all__'


class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = '__all__'


class JobSerializer(serializers.ModelSerializer):
    questionsmodel_set = QuestionsSerializer(many=True, read_only=True)

    class Meta:
        model = Job
        fields = ('id', 'title', 'questionsmodel_set', 'created_at')


class RequirementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Requirement
        fields = '__all__'


class JobRequirementSerializer(serializers.ModelSerializer):
    requirement = RequirementSerializer()

    class Meta:
        model = JobRequirement
        fields = '__all__'

    def create(self, validated_data):
        requirement_data = validated_data.pop('requirement')
        requirement_instance, created = Requirement.objects.get_or_create(**requirement_data)
        job_requirement = JobRequirement.objects.create(requirement=requirement_instance, **validated_data)
        return job_requirement
