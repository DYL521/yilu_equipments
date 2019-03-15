# -*- coding: utf-8 -*-
from django.core.cache import caches


class EquipmentCache(object):
    """
    Class that controls access to our main cache.
    """

    def __init__(self):
        self.cache = caches['default']
