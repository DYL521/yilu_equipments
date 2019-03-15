from django.db import models

from base.models import ActiveUpdateModelCommon
from equipment.const import ManufactureList
from external_api import external_api_manager
from room.models import Room, RoomTypeCommand


class EquipmentCommon(ActiveUpdateModelCommon):
    class Meta:
        abstract = True

    manufacture = models.SmallIntegerField(choices=ManufactureList.choices)
    manufacture_device_id = models.CharField(max_length=256)
    room = models.ForeignKey(Room, on_delete=models.DO_NOTHING)

    def __getattr__(self, s):
        def device_action(**kwargs):
            return self.call_provider_api(s, **kwargs)

        try:
            manufacture = ManufactureList.get_choice(self.manufacture).label
        except KeyError:
            raise AttributeError("Manufacture ID {} does not exist".format(self.manufacture))

        device_type = self.__class__.__name__.lower()
        action = s

        if manufacture not in external_api_manager.provided_functions:
            raise AttributeError("Manufacture {} does not exist".format(manufacture))

        if device_type not in external_api_manager.provided_functions[manufacture]:
            raise AttributeError("Device {} from manufacture {} does not exist".format(device_type, manufacture))

        if action not in external_api_manager.provided_functions[manufacture][device_type]:
            raise AttributeError("Action {} for Device {} from manufacture {} does not exist".format(
                action, device_type, manufacture))

        setattr(self, s, device_action)
        return getattr(self, s)

    def call_provider_api(self, action, **kwargs):
        return external_api_manager.call(self.manufacture, self.__class__.__name__.lower(),
                                         self.manufacture_device_id, action, **kwargs)
