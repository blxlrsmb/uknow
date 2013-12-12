#!/usr/bin/env python2
# -*- coding: utf-8 -*-
# $File: refresh.py
# $Date: Fri Dec 13 01:23:32 2013 +0800
# $Author: jiakai <jia.kai66@gmail.com>


from . import api_method

from ..util import get_current_user_id, login_required

from ukfetcher import get_user_fetcher_celery_task


@api_method('/refresh')
@login_required
def refresh():
    """refresh user-specified fetchers"""
    t = get_user_fetcher_celery_task()
    t(get_current_user_id())
    return {'success': 1}
