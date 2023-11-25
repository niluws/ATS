from rest_framework import serializers
from .models import Job,NewPositionModel,Requirement,JobRequirement

class BasePositionSerializer(serializers.ModelSerializer):
    class Meta:
        model = NewPositionModel
        fields = ['position_title', 'contract_type', 'reason', 'education_level', 'experience_level', 'department', 'quantity', 'budget']

            
class HRApprovalSerializer(BasePositionSerializer):
    class Meta(BasePositionSerializer.Meta):
        fields = BasePositionSerializer.Meta.fields + ['hr_approval', 'assigned_to_td','is_advertised','message']
        read_only_fields = BasePositionSerializer.Meta.fields + ['assigned_to_td']


class TDApprovalSerializer(HRApprovalSerializer):
    class Meta(HRApprovalSerializer.Meta):
        fields = HRApprovalSerializer.Meta.fields + ['interviewer', 'is_advertised','td_approval','message']
        read_only_fields = HRApprovalSerializer.Meta.fields + ['is_advertised']

class JobSerializer(serializers.ModelSerializer):
    class Meta:
        model = Job
        fields = '__all__'

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