from django.utils.translation import ugettext as _

from rest_framework import serializers
from atomization_glass.models import Glass
from room.models import Room, RoomTypeCommand
from room.models import Hotel


class GlassSerializer(serializers.ModelSerializer):
    room = serializers.PrimaryKeyRelatedField(queryset=Room.objects.all())
    room_type_command = serializers.PrimaryKeyRelatedField(queryset=RoomTypeCommand.objects.all())

    class Meta:
        model = Glass
        fields = ('manufacture', 'manufacture_device_id', 'room', 'room_type_command')


class SwitchGlassSerializer(serializers.Serializer):
    hid = serializers.IntegerField(write_only=True, help_text="Hotel ID on EFD_set")
    room_number = serializers.CharField(write_only=True, help_text="room number as given by hotel")

    def validate(self, data):
        room_instance = Room.objects.filter(
            hid__exact=data['hid'], room_number__exact=data['room_number'],is_active=True)
        if not room_instance:
            raise serializers.ValidationError(
                {"room_number": _("Hotel or Room does not exist")})

        data['glass_instance'] = Glass.objects.filter(
            room__exact=room_instance.first().id, is_active=True)
        if not data['glass_instance']:
            raise serializers.ValidationError(
                {"room_number": _("atomization glass does not exist")})

        data['command'] = data['glass_instance'].first().room_type_command.command
        data['url'] = Hotel.objects.filter(hid=data['hid'], is_active=True).first().bangqi_url
        return data
