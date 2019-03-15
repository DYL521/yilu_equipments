from django.db import models

from equipment.models import EquipmentCommon
from semantic_version.django_fields import VersionField
from base.models import ActiveUpdateModelCommon
import hashlib
from cateye.cache import CatEyeCache

import logging
logger = logging.getLogger(__name__)


class CatEye(EquipmentCommon):
    private_ip = models.GenericIPAddressField(blank=True, null=True)
    push_id = models.CharField(blank=True, max_length=128)
    software_version = VersionField(blank=True, null=True, partial=False, coerce=True)
    hardware_version = VersionField(blank=True, null=True, partial=False, coerce=True)
    last_seen = models.DateTimeField(blank=True, null=True)


class CatEyeSoftwareVersionManager(models.Manager):
    @staticmethod
    def get_latest():
        cache = CatEyeCache()
        
        latest = cache.get_latest_software_version()
        if not latest:
            all_active = CatEyeSoftwareVersion.objects.filter(is_active=True)
            if not all_active:
                logger.error("There's no active software released. Add one!")
                return None
            latest = all_active[0]
            for i in all_active[1:]:
                if i.version > latest.version:
                    latest = i
            cache.set_latest_software_version(latest)
            
        return latest

class CatEyeSoftwareVersion(ActiveUpdateModelCommon):
    version = VersionField(partial=False, coerce=True)
    apk = models.FileField(upload_to = "cateye_software")
    log = models.TextField(blank=True)
    size = models.IntegerField(editable = False)
    md5 = models.CharField(editable = False, max_length = 32)

    objects = CatEyeSoftwareVersionManager()

    def save(self, *args, **kwargs):
        self.size = self.apk.size
        self.md5 = hashlib.md5(self.apk.read()).hexdigest()
        super(CatEyeSoftwareVersion, self).save(*args, **kwargs)
        
