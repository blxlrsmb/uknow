#!/usr/bin/env python2
# -*- coding: utf-8 -*-
# $File: __init__.py
# $Date: Wed Nov 13 01:47:24 2013 +0800
# $Author: jiakai <jia.kai66@gmail.com>

"""provide fetcher background service, and also utilities for managing
fetchers"""

from .user import get_celery_task as get_user_fetcher_celery_task

# TODO: limit user connection; coroutine for different users
