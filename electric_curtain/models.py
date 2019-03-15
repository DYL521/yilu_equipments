from django.db import models
from equipment.models import EquipmentCommon
from room.models import RoomType, RoomTypeCommand
# Create your models here.


class Curtain(EquipmentCommon):
    room_type_command = models.ForeignKey(RoomTypeCommand, on_delete=models.PROTECT, null=True)

    class Meta:
        unique_together = ('room', 'room_type_command')
