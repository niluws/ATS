from rest_framework import serializers
from .models import Job,NewPositionModel
from rest_framework import serializers


class BasePositionSerializer(serializers.ModelSerializer):
    class Meta:
        model = NewPositionModel
        fields = ['position_title', 'contract_type', 'reason', 'education_level', 'experience_level', 'department', 'quantity', 'budget']

            
class HRApprovalSerializer(BasePositionSerializer):
    class Meta(BasePositionSerializer.Meta):
        fields = BasePositionSerializer.Meta.fields + ['hr_approval', 'assigned_to_td']
        read_only_fields = BasePositionSerializer.Meta.fields + ['assigned_to_td']


class TDApprovalSerializer(HRApprovalSerializer):
    class Meta(HRApprovalSerializer.Meta):
        fields = HRApprovalSerializer.Meta.fields + ['interviewer', 'is_advertised','td_approval']
        read_only_fields = HRApprovalSerializer.Meta.fields + ['is_advertised']

class JobSerializer(serializers.ModelSerializer):
    class Meta:
        model = Job
        fields = '__all__'

