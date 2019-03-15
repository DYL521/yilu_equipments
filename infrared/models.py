from django.db import models

from equipment.models import EquipmentCommon
from infrared.const import InfraredPositionChoices


class Infrared(EquipmentCommon):
    human_detected = models.BooleanField(default=True)
    last_time_human_detected = models.DateTimeField(blank=True, null=True)
    position = models.SmallIntegerField(choices=InfraredPositionChoices.choices)
