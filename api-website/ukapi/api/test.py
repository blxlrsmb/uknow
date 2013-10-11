# -*- coding: utf-8 -*-
# $File: test.py
# $Date: Fri Oct 11 22:41:24 2013 +0800
# $Author: jiakai <jia.kai66@gmail.com>

from ..base import api_method

@api_method('/test')
def test():
    return {'answer': 42}

