from django.utils.translation import ugettext as _

from rest_framework import serializers
from electric_curtain.models import Curtain
from room.models import Room, Hotel, EquipmentCode, RoomTypeCommand
from electric_curtain.const import ControlTypeChoices


class CurtainSerializer(serializers.ModelSerializer):
    room = serializers.PrimaryKeyRelatedField(queryset=Room.objects.all())
    room_type_command = serializers.PrimaryKeyRelatedField(queryset=RoomTypeCommand.objects.all())

    class Meta:
        model = Curtain
        fields = ('manufacture', 'manufacture_device_id', 'room', 'room_type_command')


class SwitchCurtainSerializer(serializers.Serializer):
    hid = serializers.IntegerField(write_only=True, help_text="Hotel ID on EFD_set")
    room_number = serializers.CharField(write_only=True, help_text="room number as given by hotel")
    control_type = serializers.IntegerField(
        write_only=True, help_text='control type, open curtain : 0; close curtains : 10; ')

    def validate(self, data):
        if int(data['control_type']) not in [i for i in ControlTypeChoices.values]:
            raise serializers.ValidationError(
                {"control_type": _("control_type does not exist")})

        room_instance = Room.objects.filter(
            hid__exact=data['hid'], room_number__exact=data['room_number'],is_active=True)
        if not room_instance:
            raise serializers.ValidationError(
                {"room_number": _("Hotel or Room does not exist")})

        data['curtain_instance'] = Curtain.objects.filter(
            room__exact=room_instance.first().id, is_active=True)
        if not data['curtain_instance']:
            raise serializers.ValidationError(
                {"room_number": _("Curtain does not exist")})

        control_type = int(data['control_type']) == ControlTypeChoices.open_curtain and '窗帘开' or '窗帘关'
        for i in data['curtain_instance']:
            if EquipmentCode.objects.filter(pk=i.room_type_command.equipment_name_id).first().code_name == control_type:
                data['command'] = i.room_type_command.command

        data['url'] = Hotel.objects.filter(hid=data['hid'], is_active=True).first().bangqi_url

        return data
