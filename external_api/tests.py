from django.test import TestCase
from rest_framework.test import APIClient

from equipment.const import ManufactureList
from infrared.models import Infrared
from light.models import Light
from infrared.models import Infrared
from room.models import Room
from room.const import RoomStatus
from infrared.const import InfraredPositionChoices
from django_api_key.models import APIKey


class ExternalManagerTests(TestCase):
    def setUp(self):
        self.api_key = APIKey.objects.create(name="test", path_re="")
        self.room = Room.objects.create(
            hid=1,
            room_number="1234",
            floor = 1,
            status = RoomStatus.available,
        )
        self.ir = Infrared.objects.create(
            manufacture=ManufactureList.dummy,
            manufacture_device_id="123",
            room = self.room,
            human_detected = False,
            position = InfraredPositionChoices.just_in_door,
        )
        
    def test_success_call(self):
        light = Light()
        light.manufacture = ManufactureList.dummy
        light.manufacture_device_id = "123"
        self.assertEqual(
            light.turn_on(),
            "I can turn on the light with device ID 123 on with kwargs {}")

    def test_success_call_with_parameters(self):
        light = Light()
        light.manufacture = ManufactureList.dummy
        light.manufacture_device_id = "123"
        self.assertEqual(
            light.turn_on(aa=1),
            "I can turn on the light with device ID 123 on with kwargs {'aa': 1}")

    def test_non_exist_manufacture(self):
        light = Light()
        light.manufacture = "non-exist"
        light.manufacture_device_id = "123"

        with self.assertRaises(AttributeError) as cm:
            light.turn_on()
        self.assertEqual(str(cm.exception), str(
            "Manufacture ID non-exist does not exist"))

    def test_non_exist_device(self):
        infrared = Infrared()
        infrared.manufacture = ManufactureList.dummy
        infrared.manufacture_device_id = "123"

        with self.assertRaises(AttributeError) as cm:
            infrared.turn_on()
        self.assertEqual(str(cm.exception), str(
            "Device infrared from manufacture dummy does not exist"))

    def test_non_exist_action(self):
        light = Light()
        light.manufacture = ManufactureList.dummy
        light.manufacture_device_id = "123"

        with self.assertRaises(AttributeError) as cm:
            light.jump()
        self.assertEqual(str(cm.exception), str(
            "Action jump for Device light from manufacture dummy does not exist"))

    def test_incoming_call_success(self):
        client = APIClient()
        response = client.post('/receiver/dummy/infrared/',
                               data = {
                                   'hid' : self.room.hid,
                                   'room_number': self.room.room_number,
                                   'position': self.ir.position,
                                   'detected': True
                               },
                               HTTP_API_KEY=self.api_key.key,
        )
        self.assertEqual(response.status_code, 200)

        self.ir.refresh_from_db()
        self.assertTrue(self.ir.human_detected)

    def test_incoming_call_on_non_exist_device(self):
        client = APIClient()
        response = client.post('/receiver/dummy/infrared/',
                               data = {
                                   'hid' : self.room.hid,
                                   'room_number': "none-exist",
                                   'position': self.ir.position,
                                   'detected': True
                               },
                               HTTP_API_KEY=self.api_key.key,
        )
        # since this is for external caller, returning status code other than 200 might cause them stop sending to us,
        # so we return 200 even when there's a data error
        self.assertEqual(response.status_code, 200)

        self.ir.refresh_from_db()
        self.assertFalse(self.ir.human_detected)
        
    def test_incoming_call_on_non_exist_device_type(self):
        client = APIClient()
        response = client.post('/receiver/dummy/none-exist/',
                               data = {
                                   'hid' : self.room.hid,
                                   'room_number': self.room.room_number,
                                   'position': self.ir.position,
                                   'detected': True
                               },
                               HTTP_API_KEY=self.api_key.key,
        )
        # calling an non-exist URL means some configuration error, so we return 404
        self.assertEqual(response.status_code, 404)
        
