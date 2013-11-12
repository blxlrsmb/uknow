#!/usr/bin/env python2
# -*- coding: utf-8 -*-
# $File: __init__.py
# $Date: Tue Nov 12 20:40:51 2013 +0800
# $Author: jiakai <jia.kai66@gmail.com>

"""user config; defaults are in stored in default.py, and can be overwritten by
user.py, which is in .gitignore"""

from .default import *

try:
    from .user import *
except ImportError:
    pass

