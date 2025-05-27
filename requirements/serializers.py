from rest_framework import serializers
from requirements.models import Requirement

class RequirementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Requirement
        fields = '__all__'
