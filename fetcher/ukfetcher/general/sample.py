#!/usr/bin/env python2
# -*- coding: utf-8 -*-
# $File: sample.py
# $Date: Wed Dec 11 18:18:39 2013 +0800
# $Author: jiakai <jia.kai66@gmail.com>

"""sample fetcher which returns a random number"""

from . import register_fetcher
from ukitem import TextOnlyItem

import random


@register_fetcher('random_fetcher')
def random_fetcher(ctx):
    ctx.new_item(TextOnlyItem('random', str(random.random())), ['random'])
