# -*- coding: utf-8 -*-
# $File: sample.py
# $Date: Fri Nov 15 21:04:50 2013 +0800
# $Author: jiakai <jia.kai66@gmail.com>

"""sample api"""

from . import api_method


@api_method('/sample')
def test():
    """api which returns the answer to life, universe and everything"""
    return {'answer': 42}
