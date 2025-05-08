from rest_framework import serializers
from labels.models import LabelTemplate

class LabelTemplateSerializer(serializers.ModelSerializer):
    class Meta:
        model = LabelTemplate
        fields = '__all__'
