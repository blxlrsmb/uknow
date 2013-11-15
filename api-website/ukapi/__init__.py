# -*- coding: utf-8 -*-
# $File: __init__.py
# $Date: Fri Nov 15 21:01:47 2013 +0800
# $Author: jiakai <jia.kai66@gmail.com>

"""unknown informatin hub API website

global variables:
    g.user_id    ID of current user (int)
"""

import os
from flask import Flask

from ukutil import import_all_modules


class DefaultConfig(object):
    API_HOST = None
    API_PORT = None
    API_RUN_OPTIONS = {}

_app = Flask(__name__,
             instance_relative_config=True,
             instance_path=os.environ.get('UKNOW_CONFIG'))
_app.config.from_object(DefaultConfig())


def get_app():
    """load API modules and return the WSGI application"""
    global get_app
    import_all_modules(__file__, __name__)
    get_app = lambda: _app
    return get_app()
