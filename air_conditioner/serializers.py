from django.utils.translation import ugettext as _

from air_conditioner.models import AirConditioner
from rest_framework import serializers
from room.models import Room, Hotel
from air_conditioner.const import AirConditionerModeChoices, WindDirectionChoices, WindSpeedChoices


class AirConditionerSerializer(serializers.ModelSerializer):
    class Meta:
        model = AirConditioner
        fields = '__all__'


class ACCommonSerializer(serializers.Serializer):
    hid = serializers.IntegerField(write_only=True, help_text="Hotel ID on EFD_set")
    room_number = serializers.CharField(write_only=True, help_text="room number as given by hotel")

    def validate(self, data):
        room_instance = Room.objects.filter(
            hid__exact=data['hid'], room_number__exact=data['room_number'], is_active=True)
        if not room_instance:
            raise serializers.ValidationError(
                {"room_number": _("Hotel or Room does not exist")})

        if 'wind_direction' in data.keys():
            available_ac_direction = [x[0] for x in WindDirectionChoices.choices]
            if data['wind_direction'] not in available_ac_direction:
                raise serializers.ValidationError(
                    {"wind_direction": _("only {} is allowed").format(available_ac_direction)})

        elif 'mode' in data.keys():
            available_ac_mode = [x[0] for x in AirConditionerModeChoices.choices]
            if data['mode'] not in available_ac_mode:
                raise serializers.ValidationError(
                    {"mode": _("only {} is allowed").format(available_ac_mode)})

        elif 'wind_speed' in data.keys():
            available_ac_speed = [x[0] for x in WindSpeedChoices.choices]
            if data['wind_speed'] not in available_ac_speed:
                raise serializers.ValidationError(
                    {"wind_speed": _("only {} is allowed").format(available_ac_speed)})

        elif 'temperature' in data.keys():
            if not 16 <= data['temperature'] <= 30:
                raise serializers.ValidationError(
                    {"temperature": _("only 16~30 is allowed")})

        data['air_conditioner_instance'] = AirConditioner.objects.filter(
            room__exact=room_instance.first().id, is_active=True)
        if not data['air_conditioner_instance']:
            raise serializers.ValidationError(
                {"room_number": _("air conditioner does not exist")})

        hotel_instance = Hotel.objects.filter(hid=data['hid'], is_active=True)
        if not hotel_instance:
            raise serializers.ValidationError(
                {"hid": _("Hotel does not exist or is_active is false")})

        data['air_conditioner_address'] = data['air_conditioner_instance'].first().manufacture_device_id
        data['url'] = Hotel.objects.filter(hid=data['hid'], is_active=True).first().samsung_ac_url

        if not data['url']:
            raise serializers.ValidationError(
                {"samsung_ac_url": _("Hotel samsung_ac_url does not exist")})

        return data

    def update(self, instance, validated_data):
        instance.wind_direction = list(WindDirectionChoices.values.keys()) [list(WindDirectionChoices.labels.values()).
                                      index(validated_data['wind_direction'].replace('_', ' '))]
        instance.wind_speed = list(WindSpeedChoices.values.keys()) [list(WindSpeedChoices.labels.values()).
                                  index(validated_data['wind_speed'].replace('_', ' '))]
        instance.mode = list(AirConditionerModeChoices.values.keys())[list(AirConditionerModeChoices.labels.values()).
                            index(validated_data['mode'].replace('_', ' '))]
        instance.temperature = validated_data['temperature']
        instance.room_temperature = validated_data['room_temperature']
        instance.is_on = validated_data['is_on']
        instance.save()
        return validated_data

    def convert_enum(self, query_data):
        query_data['wind_direction'] = list(WindDirectionChoices.values.keys()) [
            list(WindDirectionChoices.labels.values()).index(query_data['wind_direction'].replace('_', ' '))]
        query_data['wind_speed'] = list(WindSpeedChoices.values.keys()) [
            list(WindSpeedChoices.labels.values()).index(query_data['wind_speed'].replace('_', ' '))]
        query_data['mode'] = list(AirConditionerModeChoices.values.keys()) [
            list(AirConditionerModeChoices.labels.values()).index(query_data['mode'].replace('_', ' '))]
        del query_data['url']
        return query_data


class ChangeModeSerializer(ACCommonSerializer):
    mode = serializers.IntegerField(write_only=True,
                                    help_text="Air conditioning mode set by user, not_sure:0; auto:10; cold:20; "
                                              "dehumidification:30; fan:40; warm:50")


class ACSwitchSerializer(ACCommonSerializer):
    switch = serializers.BooleanField(write_only=True, help_text="Air conditioner switch, 0:close; 1:run;")


class ChangeDirectionSerializer(ACCommonSerializer):
    wind_direction = serializers.IntegerField(write_only=True,
                                              help_text=_("Wind direction, not_sure:0; up_and_down:10; "
                                                          "left_and_right:20; around:30; stop:40"))


class ChangeSpeedSerializer(ACCommonSerializer):
    wind_speed = serializers.IntegerField(write_only=True,
                                          help_text=_("Wind speed, not_sure:0; auto:10; slow:20; medium:30; quick:40"))


class ChangeTemperatureSerializer(ACCommonSerializer):
    temperature = serializers.IntegerField(write_only=True, help_text=_("Set the air conditioning temperature, "
                                                                        "only 16~30 is allowed"))
