from django.db import models
from equipment.models import EquipmentCommon
from room.models import RoomTypeCommand
# Create your models here.


class Glass(EquipmentCommon):
    room_type_command = models.ForeignKey(RoomTypeCommand, on_delete=models.PROTECT, null=True)

    class Meta:
        unique_together = ('room', 'room_type_command')
