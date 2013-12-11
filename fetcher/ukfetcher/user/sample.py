#!/usr/bin/env python2
# -*- coding: utf-8 -*-
# $File: sample.py
# $Date: Wed Dec 11 20:01:55 2013 +0800
# $Author: jiakai <jia.kai66@gmail.com>

"""sample user fetcher"""

from . import register_fetcher

from ukitem import TextOnlyItem


@register_fetcher('sample_user')
def sample_user_fetcher(ctx):
    """say hello"""
    ctx.new_item(TextOnlyItem('hello', str(ctx.user_id)), ['hello'])
