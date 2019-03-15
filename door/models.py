from django.db import models

from door.const import DoorOpenDirectionChoices, LockOpenMethodChoices
from room.models import Room
from equipment.models import EquipmentCommon
from base.models import ActiveUpdateModelCommon


class Door(EquipmentCommon):
    """A virtual equipment, which not "smart" actually."""
    is_opened = models.NullBooleanField(default=None)  # null means we are not sure
    open_direction = models.SmallIntegerField(
        choices=DoorOpenDirectionChoices.choices, default=DoorOpenDirectionChoices.not_sure)


class Lock(EquipmentCommon):
    is_opened = models.NullBooleanField(default=None)  # null means we are not sure


class DoorSensor(EquipmentCommon):
    is_opened = models.NullBooleanField(default=None)  # null means we are not sure
    open_method = models.SmallIntegerField(
        choices=LockOpenMethodChoices.choices, default=LockOpenMethodChoices.not_sure)


class UserUnlockTime(ActiveUpdateModelCommon):
    room = models.ForeignKey(Room, on_delete=models.DO_NOTHING)
    card_type = models.SmallIntegerField(
        choices=LockOpenMethodChoices.choices, default=LockOpenMethodChoices.not_sure)
    card_data = models.CharField(max_length=256)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    
