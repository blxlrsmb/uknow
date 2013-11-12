#!/usr/bin/env python2
# -*- coding: utf-8 -*-
# $File: sample.py
# $Date: Wed Nov 13 01:32:52 2013 +0800
# $Author: jiakai <jia.kai66@gmail.com>

"""a sample prefilter"""

from . import prefilter
import time

@prefilter("sample")
def sample(ctx, doc):
    """add `passed by sample' to desc"""
    doc["desc"] += " [passed by sample system]"

@prefilter("sample_user", is_user = True)
def sample(ctx, doc):
    """add `passed by sample' to desc"""
    print 'slow async task ...'
    time.sleep(1)
    doc["desc"] += " [passed by sample user, for uid {}]".format(
            ctx.user_id)

