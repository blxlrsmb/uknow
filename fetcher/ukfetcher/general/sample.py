#!/usr/bin/env python2
# -*- coding: utf-8 -*-
# $File: sample.py
# $Date: Tue Nov 12 23:45:11 2013 +0800
# $Author: jiakai <jia.kai66@gmail.com>

"""sample fetcher which returns a random number"""

from  . import register_fetcher

import random

@register_fetcher('random_fetcher')
def random_fetcher(ctx):
    ctx.new_item('random {}'.format(random.random()), ['random'])

