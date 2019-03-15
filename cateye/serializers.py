import base64
import json
import urllib

from django.conf import settings
from django.utils.translation import ugettext as _
from django.utils.timezone import now
from rest_framework.reverse import reverse

import requests
from cateye.models import CatEye, CatEyeSoftwareVersion
from door.models import Lock
from equipment.const import ManufactureList
from rest_framework import serializers
import semantic_version 

import logging
logger = logging.getLogger(__name__)

from cateye.cache import CatEyeCache
cache = CatEyeCache()

class CatEyeSerializer(serializers.ModelSerializer):
    class Meta:
        model = CatEye
        fields = '__all__'


class CatEyeDeviceIDMixin(object):
    def validate_manufacture_device_id(self, value):
        """
        Check this device exisit.
        """
        if CatEye.objects.filter(manufacture_device_id=value).count() == 0:
            raise serializers.ValidationError(_("This device ID does not exist"))

        self.cateye = CatEye.objects.get(
            manufacture=ManufactureList.yilu,
            manufacture_device_id=value)

        return value


class CatEyeUpdateSerializer(CatEyeDeviceIDMixin, serializers.ModelSerializer):
    room_number = serializers.SerializerMethodField()
    update_info = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = CatEye
        fields = ['manufacture_device_id', 'private_ip', 'push_id', 'room_number', 'software_version',
                  'hardware_version', 'update_info']

    def validate_software_version(self, value):
        if not semantic_version.validate(value):
            raise serializers.ValidationError(_("Not valid version string"))
        return semantic_version.Version(value)
        
    def validate_hardware_version(self, value):
        if not semantic_version.validate(value):
            raise serializers.ValidationError(_("Not valid version string"))
        return semantic_version.Version(value)
        
    def save(self):
        self.instance = CatEye.objects.get(
            manufacture=ManufactureList.yilu,
            manufacture_device_id=self.validated_data['manufacture_device_id'])
        self.instance.private_ip = self.validated_data['private_ip']
        self.instance.push_id = self.validated_data['push_id']
        self.instance.software_version = self.validated_data['software_version']
        self.instance.hardware_version = self.validated_data['hardware_version']
        self.instance.save()
        
        return self.instance

    def get_room_number(self, obj):
        return self.instance.room.room_number

    def get_update_info(self, obj):
        latest = CatEyeSoftwareVersion.objects.get_latest()
        if not latest or latest.version <= self.instance.software_version:
            return None
        return reverse("cateyesoftwareversion-detail", args=[latest.id,])


class CatEyePingSerializer(CatEyeDeviceIDMixin, serializers.ModelSerializer):
    class Meta:
        model = CatEye
        fields = ['manufacture_device_id',]
        
    def validate_manufacture_device_id(self, value):
        if cache.get_device_id_last_seen(value):
            return value
        else:
            return super(CatEyePingSerializer, self).validate_manufacture_device_id(value)

    def save(self):
        cache.set_device_id_last_seen(self.validated_data['manufacture_device_id'], now())
        logger.debug("cateye for hid {}, room number {} is pinging".format(self.cateye.room.hid, self.cateye.room.room_number))
        
    
class FaceRecognitionSerializer(CatEyeDeviceIDMixin, serializers.Serializer):
    manufacture_device_id = serializers.CharField(max_length=256, write_only=True)
    color_image = serializers.ImageField(write_only=True)
    black_white_image = serializers.ImageField(write_only=True)

    def _fetch_guest_info(self):
        url = urllib.parse.urljoin(settings.BOOKING_API_URL, "/hotel/regist/findRegistMsgForOtherPms.do")
        headers = {
            "Content-Type": "application/json",
        }
        payload = {
            "sessionToken": "CATEYE",
            "roomNo": self.cateye.room.room_number,
            "hid": self.cateye.room.hid,
        }
        logger.debug("cateye is for hid {}, room number {}".format(self.cateye.room.hid, self.cateye.room.room_number))
        
        response = requests.get(url, params=payload, headers=headers)
        logger.debug("response from booking: {}".format(response.content.decode('utf-8')))
        return json.loads(response.content.decode('utf-8'))

    def validate_manufacture_device_id(self, value):
        device_id = super(FaceRecognitionSerializer, self).validate_manufacture_device_id(value)
        logger.debug("device_id: {}".format(device_id))

        try:
            self.lock = Lock.objects.get(room=self.cateye.room)
            logger.debug("lock ID: {}".format(self.lock.manufacture_device_id))
        except Lock.DoesNotExist:
            raise serializers.ValidationError(_("There's no lock for this room"))

        return device_id

    def _check_if_is_this_person(self, s, url, payload, image):
        payload.update({"image_url1": image})
        response = s.post(url, data=payload)
        logger.debug("response from face++: {}".format(response.content))
        result = json.loads(response.content)
        if "confidence" in result and result['confidence'] > result["thresholds"][settings.FACEPP_THRESH_HOLD]:
            lock_result = self.lock.open_lock()
            logger.debug("result from lock: {}".format(lock_result))
            return True
        else:
            return False
    
    def check_face(self):
        guests_info = self._fetch_guest_info()
        if 'guestList' not in guests_info:
            logger.info("No one is living in room {} of hotel ID {}, do NOT open the door".format(
                self.cateye.room.room_number, self.cateye.room.hid))
            return False, _("No one is living in this room")
        else:
            guestList = guests_info['guestList']
            logger.debug("guest list: {}".format(guestList))

        url = urllib.parse.urljoin(settings.FACEPP_API_URL, "/facepp/v3/compare")
        color_image_encoded = base64.b64encode(self.validated_data['color_image'].read())
        black_white_image_encoded = base64.b64encode(self.validated_data['black_white_image'].read())

        with requests.Session() as s:
            # check if the two images match
            logger.debug("Checking if the color and black-white images match")
            payload = {
                "api_key": settings.FACEPP_API_KEY,
                "api_secret": settings.FACEPP_API_SECRET,
                "image_base64_1": black_white_image_encoded,
                "image_base64_2": color_image_encoded,
            }
            response = s.post(url, data=payload)
            logger.debug("response from face++: {}".format(response.content))
            result = json.loads(response.content)
            if len(result['faces2']) == 0:
                logger.debug("There's no face in the image, ignore checking")
                return False, _("There's no face in the image")
            else:
                face2_token = result['faces2'][0]['face_token']
                payload.pop('image_base64_1', None)
                payload.pop('image_base64_2', None)
                payload.update({"face_token2": face2_token})

            if ("confidence" not in result) or result['confidence'] < result["thresholds"][settings.FACEPP_THRESH_HOLD]:
                logger.critical("Normal and Infrared camera doesn't match for room {} of hotel ID {}. Possible facial "
                                "attack!".format(self.cateye.room.room_number, self.cateye.room.hid))
                return False, _("Normal and Infrared camera doesn't match. This has been reported.")

            for guest in guestList:
                if self._check_if_is_this_person(s, url, payload, guest["cameraImage"] or guest['idImage']):
                    logger.debug("{} is living in this room, open the door".format(guest['name']))
                    return True, "success"

            for user in settings.INTERNAL_USERS_OPEN_ALL_DOORS:
                if self._check_if_is_this_person(s, url, payload, user[1]):
                    logger.debug("{} is an internal user, open the door".format(user[0]))
                    return True, "success"
                
        return False, _("Can't recognize this face")

class CatEyeSoftwareVersionSerializer(serializers.ModelSerializer):
    class Meta:
        model = CatEyeSoftwareVersion
        fields = '__all__'
