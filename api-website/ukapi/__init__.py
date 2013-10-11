# -*- coding: utf-8 -*-
# $File: __init__.py
# $Date: Fri Oct 11 23:06:24 2013 +0800
# $Author: jiakai <jia.kai66@gmail.com>

"""unknown informatin hub API website

global variables:
    g.api_key_id    ID of api key (int)
"""

from flask import Flask

from importlib import import_module
from pkgutil import walk_packages
import os

_app = Flask(__name__)

def get_app():
    """load API modules and return the WSGI application"""
    global get_app
    for loader, module_name, is_pkg in walk_packages(
            [os.path.dirname(__file__)], __name__ + '.'):
        import_module(module_name)

    get_app = lambda: _app
    return get_app()

