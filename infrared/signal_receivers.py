from django.utils import timezone

from infrared.models import Infrared
from room.const import RoomStatus
from room.models import Room


def infrared_detected_human_receiver(sender, **kwargs):
    try:
        room = Room.objects.get(hid=kwargs['hid'], room_number=kwargs['room_number'])
        ir = Infrared.objects.get(room=room, position=kwargs['position'])
    except (Room.DoesNotExist, Infrared.DoesNotExist):
        # should log an error
        return

    if kwargs['detected']:
        ir.human_detected = True
        ir.last_time_human_detected = timezone.now()
        ir.save()

        room.status = RoomStatus.people_in
        room.save()
    else:
        ir.human_detected = False
        ir.save()
