# -*- coding: utf-8 -*-
# $File: __init__.py
# $Date: Tue Dec 10 11:10:32 2013 +0800
# $Author: jiakai <jia.kai66@gmail.com>

"""unknown informatin hub API website

global variables:
    g.user_id    ID of current user (int)
"""

import os
from flask import Flask

from flask_login import LoginManager

from ukutil import import_all_modules


class DefaultConfig(object):
    API_HOST = None
    API_PORT = None
    API_RUN_OPTIONS = {}

_app = Flask(__name__,
             instance_relative_config=True,
             instance_path=os.environ.get('UKNOW_CONFIG'))
_app.config.from_object(DefaultConfig())

_app.secret_key = 'WTF is this!!'       # Should have this to work

login_manager = LoginManager()
login_manager.init_app(_app)


def get_app():
    """load API modules and return the WSGI application"""
    global get_app
    import_all_modules(__file__, __name__)
    get_app = lambda: _app
    return get_app()
