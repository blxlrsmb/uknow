#!/usr/bin/env python2
# -*- coding: utf-8 -*-
# $File: ukutil.py
# $Date: Tue Nov 12 21:01:10 2013 +0800
# $Author: jiakai <jia.kai66@gmail.com>

"""common utility functions"""

from importlib import import_module
from pkgutil import walk_packages
import os

def import_all_modules(file_path, pkg_name):
    """import all modules recursively in a package
    :param file_path: just pass __file__
    :param pkg_name: just pass __name__
    """
    for _, module_name, _ in walk_packages(
            [os.path.dirname(file_path)], pkg_name + '.'):
        import_module(module_name)

