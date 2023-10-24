from rest_framework import serializers

from .models import NewPositionModel


class NewPositionSerializer(serializers.ModelSerializer):
    class Meta:
        model = NewPositionModel
        fields = ['position_title', 'contract_type', 'reason', 'education_level', 'experience_level', 'department',
                  'quantity','budget']
