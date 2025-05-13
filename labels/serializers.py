from rest_framework import serializers
from labels.models import LabelTemplate

class LabelTemplateSerializer(serializers.ModelSerializer):
    class Meta:
        model = LabelTemplate
        fields = '__all__'

        
    def to_internal_value(self, data):
        for key, value in data.items():
            if value == "":
                data[key] = None
        return super().to_internal_value(data)
