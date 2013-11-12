# -*- coding: utf-8 -*-
# $File: __init__.py
# $Date: Tue Nov 12 21:03:06 2013 +0800
# $Author: jiakai <jia.kai66@gmail.com>

"""unknown informatin hub API website

global variables:
    g.user_id    ID of current user (int)
"""

from ukutil import import_all_modules

from flask import Flask

_app = Flask(__name__)

def get_app():
    """load API modules and return the WSGI application"""
    global get_app
    import_all_modules(__file__, __name__)
    get_app = lambda: _app
    return get_app()

