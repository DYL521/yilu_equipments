from django.utils.translation import ugettext as _

from door.models import Door, DoorSensor, Lock, UserUnlockTime
from rest_framework import serializers
from room.models import Room
from door.const import LockOpenMethodChoices, ServerLockOpenMethodChoices
from equipment.const import ManufactureList


class DoorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Door
        fields = '__all__'


class LockSerializer(serializers.ModelSerializer):
    room_id = serializers.IntegerField()
    class Meta:
        model = Lock
        fields = ('room_id', 'manufacture', 'manufacture_device_id')

    def validate(self, data):
        lock_instance = Lock.objects.filter(manufacture=data['manufacture'],
                                            manufacture_device_id=data['manufacture_device_id'])
        if lock_instance:
            raise serializers.ValidationError(
                {"lock": _("lock already exist")})
        return data


class DoorSensorSerializer(serializers.ModelSerializer):
    class Meta:
        model = DoorSensor
        fields = '__all__'


class RemoteOpenLockSerializer(serializers.Serializer):
    hid = serializers.IntegerField(write_only=True, help_text="Hotel ID on EFD_set")
    room_number = serializers.CharField(write_only=True, help_text="room number as given by hotel")

    def validate(self, data): # Hid == 222 room_number=0109
        room_instance = Room.objects.filter(hid__exact=data['hid'], room_number__exact=data['room_number'])
        if not room_instance:
            raise serializers.ValidationError(
                {"room_number": _("Hotel or Room does not exist")})

        data['lock_instance'] = Lock.objects.filter(room__exact=room_instance.first().id, is_active=True)
        if not data['lock_instance']:
            raise serializers.ValidationError(
                {"room_number": _("Lock does not exist")})

        for manufacture_number in ManufactureList.values:
            if data['lock_instance'].first().manufacture == manufacture_number:
                data['lock_manufacture'] = ManufactureList.values[manufacture_number]

        if not data['lock_manufacture']:
            raise serializers.ValidationError(
                {"lock_manufacture": _("LockManufacture does not exist")})

        return data

    def update(self, instance, validated_data):
        UserUnlockTime.objects.filter(room__exact=instance, is_active=True).update(is_active=False)
        return validated_data


class DeleteOpenUserSerializer(RemoteOpenLockSerializer):
    CardType = serializers.CharField(write_only=True,
                                     help_text="Type of door opening: 1, room card 2, id card 3, password")
    CardData = serializers.CharField(write_only=True, help_text="Hotel Card data")

    def validate(self, data):
        super().validate(data)

        if int(data['CardType']) not in [i for i in ServerLockOpenMethodChoices.values]:
            raise serializers.ValidationError(
                {"CardType": _("CardType does not exist")})

        return data

    def update(self, instance, validated_data):
        if validated_data['CardType'] == str(ServerLockOpenMethodChoices.hotel_card):
            card_type = LockOpenMethodChoices.hotel_card

        elif validated_data['CardType'] == str(ServerLockOpenMethodChoices.ID_card):
            card_type = LockOpenMethodChoices.ID_card

        else:
            card_type = LockOpenMethodChoices.password

        UserUnlockTime.objects.filter(room__exact=instance, card_type=card_type, card_data=validated_data['CardData']) \
            .update(is_active=False)

        return validated_data


class UserCardSerializer(DeleteOpenUserSerializer):
    BeginTime = serializers.DateTimeField(write_only=True, help_text="You can use the start time of the room")
    EndTime = serializers.DateTimeField(write_only=True, help_text="You can use the end time of the room")

    def create(self, validated_data):
        if validated_data['CardType'] == str(ServerLockOpenMethodChoices.hotel_card):
            card_type = LockOpenMethodChoices.hotel_card

        elif validated_data['CardType'] == str(ServerLockOpenMethodChoices.ID_card):
            card_type = LockOpenMethodChoices.ID_card

        else:
            card_type = LockOpenMethodChoices.password

        UserUnlockTime.objects.create(
            room=Room.objects.get(hid__exact=validated_data['hid'], room_number__exact=validated_data['room_number']),
            card_type=card_type,
            card_data=validated_data['CardData'],
            start_time=validated_data['BeginTime'],
            end_time=validated_data['EndTime']
        )

        return validated_data


class QueryOpenLockLogSerializer(RemoteOpenLockSerializer):
    BeginTime = serializers.DateTimeField(write_only=True, help_text="Query start time")
    EndTime = serializers.DateTimeField(write_only=True, help_text="Query end time")
