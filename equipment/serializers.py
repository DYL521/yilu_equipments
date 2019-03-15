from django.utils.translation import ugettext as _

from room.models import EquipmentCode
from rest_framework import serializers

class EquipmentCodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = EquipmentCode
        fields = '__all__'

    def validate(self, data):
        data['is_active'] = True
        return data
