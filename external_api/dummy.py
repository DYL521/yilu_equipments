from external_api.base import ExternalAPIBase
from external_api.signals import infrared_detected_human


class Dummy(ExternalAPIBase):
    MANUFACTURE = "dummy"

    def provide_light_turn_on(self, device_id, **kwargs):
        result = "I can turn on the light with device ID {} on with kwargs {}".format(device_id, kwargs)
        return result

    def receiver_main(self, request):
        result = "I've received {} from the manufacture".format(request.data)
        print(result)

    def receiver_infrared(self, request):
        """Assuming the manufacture will send us a json if infrared status changed."""
        data = request.data
        infrared_detected_human.send(sender=self.__class__,
                                     hid=data['hid'],
                                     room_number=data['room_number'],
                                     position=data['position'],
                                     detected=data['detected'],
                                     )
