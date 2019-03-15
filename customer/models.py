from django.db import models

from base.models import ActiveUpdateModelCommon
from customer.const import PMSChoices
from room.models import Room


class Order(ActiveUpdateModelCommon):
    PMS_type = models.SmallIntegerField(choices=PMSChoices.choices, default=PMSChoices.lvyun)
    PMS_ID = models.CharField(max_length=256)
    start = models.DateTimeField()
    end = models.DateTimeField()

    def __str__(self):
        return self.PMS_ID


class StayInfo(ActiveUpdateModelCommon):
    order = models.ForeignKey(Order, on_delete=models.DO_NOTHING)
    customer_id = models.CharField(max_length=256, help_text="ID in the main customer database")
    room = models.ForeignKey(Room, on_delete=models.DO_NOTHING)
