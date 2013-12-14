#!/usr/bin/env python2
# -*- coding: utf-8 -*-
# $File: ukutil.py
# $Date: Sat Dec 14 18:01:43 2013 +0800
# $Author: jiakai <jia.kai66@gmail.com>

"""common utility functions"""

from importlib import import_module
from pkgutil import walk_packages
import os


def ensure_unicode(s):
    """assert type of s is basestring and convert s to unicode"""
    assert isinstance(s, basestring), 's should be string'
    if isinstance(s, str):
        s = s.decode('utf-8')
    return s


def import_all_modules(file_path, pkg_name):
    """import all modules recursively in a package
    :param file_path: just pass __file__
    :param pkg_name: just pass __name__
    """
    for _, module_name, _ in walk_packages(
            [os.path.dirname(file_path)], pkg_name + '.'):
        import_module(module_name)


def is_in_unittest():
    """return whether currently in unittest mode"""
    return os.getenv('IN_UKNOW_TEST') is not None
