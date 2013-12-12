#!/usr/bin/env python2
# -*- coding: utf-8 -*-
# $File: sample.py
# $Date: Thu Dec 12 15:51:41 2013 +0800
# $Author: jiakai <jia.kai66@gmail.com>

"""a sample prefilter"""

from . import prefilter
import time


@prefilter("sample")
def sample(ctx, doc):
    """add `passed by sample' to desc"""
    doc["desc"].content += " [passed by sample system]"


@prefilter("sample_user", is_user=True)
def sample(ctx, doc):
    """add `passed by sample' to desc"""
    print 'slow async task ...'
    time.sleep(1)
    doc["desc"].content += " [passed by sample user, for uid {}]".format(
        ctx.user_id)


@prefilter('auto_tag')
def auto_tag(ctx, doc):
    """auto tag """
