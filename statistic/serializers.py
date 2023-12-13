from rest_framework import serializers

from candidate.models import StatusModel


class StatusModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = StatusModel
        fields = '__all__'
