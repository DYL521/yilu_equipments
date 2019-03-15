# -*- coding: utf-8 -*-

from __future__ import division, print_function, unicode_literals


class CacheExpiryTime(object):
    """
    Class that contains most common expiry times used when caching data.
    """

    ONE_MINUTE = 60
    FIVE_MINUTES = ONE_MINUTE * 5
    TEN_MINUTES = ONE_MINUTE * 10
    FIFTEEN_MINUTES = ONE_MINUTE * 15
    THIRTY_MINUTES = TEN_MINUTES * 3
    ONE_HOUR = THIRTY_MINUTES * 2
    ONE_DAY = ONE_HOUR * 24
    ONE_WEEK = ONE_DAY * 7
    ONE_MONTH = ONE_DAY * 30
    ONE_YEAR = ONE_DAY * 365
