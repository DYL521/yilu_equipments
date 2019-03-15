from __future__ import absolute_import, unicode_literals

import datetime
import logging

from django.utils.timezone import now

from cateye.cache import CatEyeCache
from cateye.models import CatEye
from celery import shared_task

logger = logging.getLogger(__name__)

cache = CatEyeCache()

@shared_task
def sync_last_seen():
    for cateye in CatEye.objects.filter(is_active=True).iterator():
        last_seen = cache.get_device_id_last_seen(cateye.manufacture_device_id)
        if not last_seen:
            logger.warning("We don't have a record for last seen time of cateye with ID {}, might be it just got"
                           "online, or we need to increase the space of cache".format(cateye.manufacture_device_id))
        else:
            cateye.last_seen = last_seen
            cateye.save()
            if now() - last_seen > datetime.timedelta(minutes=5):
                logger.critical("We haven't seen cateye with ID {} for more than 5 minutes, go check it!".format(
                    cateye.manufacture_device_id))
