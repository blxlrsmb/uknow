# -*- coding: utf-8 -*-
# $File: sample.py
# $Date: Tue Nov 12 20:02:54 2013 +0800
# $Author: jiakai <jia.kai66@gmail.com>

"""sample api"""

from . import api_method

@api_method('/sample')
def test():
    """api which returns the answer to life, universe and everything"""
    return {'answer': 42}

