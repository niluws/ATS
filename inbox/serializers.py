from rest_framework import serializers

from .models import NewPositionModel


class NewPositionSerializer(serializers.ModelSerializer):
    class Meta:
        model = NewPositionModel
        fields = ['position_title', 'contract_type', 'reason', 'education_level', 'experience_level', 'department',
                  'quantity','budget']
        
class HRApprovalSerializer(serializers.ModelSerializer):
    class Meta:
        model = NewPositionModel
        fields = ['position_title', 'contract_type', 'reason', 'education_level', 'experience_level', 'department',
                  'quantity','budget','hr_approval','assigned_to_td']

        read_only_fields=['position_title', 'contract_type', 'reason', 'education_level', 'experience_level', 'department',
                  'quantity','budget','assigned_to_td']
        
class TDApprovalSerializer(serializers.ModelSerializer):
    class Meta:
        model = NewPositionModel
        fields = ['position_title', 'contract_type', 'reason', 'education_level', 'experience_level', 'department',
                  'quantity','budget','hr_approval','assigned_to_td','interviewer']

        read_only_fields=['position_title', 'contract_type', 'reason', 'education_level', 'experience_level', 'department',
                  'quantity','budget','assigned_to_td']