#!/usr/bin/env python2
# -*- coding: utf-8 -*-
# $File: sample.py
# $Date: Wed Nov 13 01:34:52 2013 +0800
# $Author: jiakai <jia.kai66@gmail.com>

"""sample user fetcher"""

from . import register_fetcher


@register_fetcher('sample_user')
def sample_user_fetcher(ctx):
    """say hello"""
    ctx.new_item('hello {}'.format(ctx.user_id), ['hello'])
