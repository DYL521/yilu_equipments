from django.db import models

from air_conditioner.const import AirConditionerModeChoices, WindDirectionChoices, WindSpeedChoices
from equipment.models import EquipmentCommon


class AirConditioner(EquipmentCommon):
    is_on = models.NullBooleanField(default=None)
    mode = models.SmallIntegerField(choices=AirConditionerModeChoices.choices,
                                    default=AirConditionerModeChoices.not_sure)
    temperature = models.SmallIntegerField(default=25)
    room_temperature = models.SmallIntegerField()
    wind_direction = models.SmallIntegerField(choices=WindDirectionChoices.choices,
                                              default=WindDirectionChoices.not_sure)
    wind_speed = models.SmallIntegerField(choices=WindSpeedChoices.choices,
                                              default=WindSpeedChoices.not_sure)

    class Meta:
        unique_together = ('manufacture', 'manufacture_device_id', 'room')
