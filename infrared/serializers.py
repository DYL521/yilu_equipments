from infrared.models import Infrared
from rest_framework import serializers


class InfraredSerializer(serializers.ModelSerializer):
    class Meta:
        model = Infrared
        fields = '__all__'
