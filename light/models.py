from django.db import models

from equipment.models import EquipmentCommon
from room.models import RoomTypeCommand
from light.const import LightPositionChoices


class Light(EquipmentCommon):
    is_on = models.NullBooleanField(default=None)
    room_type_command = models.ForeignKey(RoomTypeCommand, on_delete=models.PROTECT, null=True)
    position = models.SmallIntegerField(choices=LightPositionChoices.choices, default=LightPositionChoices.other)

    class Meta:
        unique_together = ('room', 'room_type_command')
