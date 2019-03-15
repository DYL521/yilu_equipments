from django.utils.translation import ugettext as _

from light.models import Light
from rest_framework import serializers
from light.const import LightPositionChoices
from room.models import Room, Hotel, EquipmentCode, RoomTypeCommand

class LightSerializer(serializers.ModelSerializer):
    room = serializers.PrimaryKeyRelatedField(queryset=Room.objects.all())
    room_type_command = serializers.PrimaryKeyRelatedField(queryset=RoomTypeCommand.objects.all())

    class Meta:
        model = Light
        fields = ('manufacture', 'manufacture_device_id', 'room', 'room_type_command')


class LightUpOrOffSerializer(serializers.Serializer):
    hid = serializers.IntegerField(write_only=True, help_text="Hotel ID on EFD_set")
    room_number = serializers.CharField(write_only=True, help_text="room number as given by hotel")
    light_position = serializers.IntegerField(
        write_only=True, help_text='''light position, 10:night_lamp; 20:porch_lamp; 30:toilet; 
        40:bed_room_main; 50:by_wall_left; 60:by_wall_right; 70:sleep_mode.''')

    def validate(self, data):
        if int(data['light_position']) not in [i for i in LightPositionChoices.values]:
            raise serializers.ValidationError(
                {"light_position": _("light_position does not exist")})

        room_instance = Room.objects.filter(
            hid__exact=data['hid'], room_number__exact=data['room_number'],is_active=True)
        if not room_instance:
            raise serializers.ValidationError(
                {"room_number": _("Hotel or Room does not exist")})

        data['light_instance'] = Light.objects.filter(
            room__exact=room_instance.first().id, is_active=True)
        if not data['light_instance']:
            raise serializers.ValidationError(
                {"room_number": _("light does not exist")})

        control_type = LightPositionChoices.values[int(data['light_position'])]
        for i in data['light_instance']:
            if EquipmentCode.objects.filter(pk=i.room_type_command.equipment_name_id).first().code_name == control_type:
                data['command'] = i.room_type_command.command

        if not data['command']:
            raise serializers.ValidationError(
                {"command": _("command does not exist")})

        data['url'] = Hotel.objects.filter(hid=data['hid'], is_active=True).first().bangqi_url
        return data


class WXLightSerializer(serializers.Serializer):
    hid = serializers.IntegerField(write_only=True, help_text="Hotel ID on EFD_set")
    room_number = serializers.CharField(write_only=True, help_text="room number as given by hotel")

    def validate(self, data):
        room_instance = Room.objects.filter(hid__exact=data['hid'], room_number__exact=data['room_number'])
        if not room_instance:
            raise serializers.ValidationError(
                {"room_number": _("Hotel or Room does not exist")})

        data['room_instance'] = room_instance.first()
        return data

    def light(self, data):
        light = Light.objects.filter(room = data['room_instance'])
        light_list = [x.position for x in light]
        room_light = []
        for (key, value) in LightPositionChoices.values.items():
            status = key in light_list and True or False
            room_light.append(dict(name = value, type = key, status = status))
        return {'light':room_light}
