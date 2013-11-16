#!/usr/bin/env python2
# -*- coding: utf-8 -*-
# $File: default.py
# $Date: Sat Nov 16 19:58:34 2013 +0800
# $Author: jiakai <jia.kai66@gmail.com>

"""default config values"""

general_fetcher_sleep_interval_default = 10
"""interval for each general fetcher to sleep between consecutive fetches"""

general_fetcher_sleep_interval_special = {
}
"""overwrite default settings, fetcher name => value"""

celery_broker = 'redis://localhost:6379/0'

mongo_conn = ('127.0.0.1', 27017)
mongo_db = 'uknow'
