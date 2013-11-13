import os
import os.path

from flask import Flask


class DefaultConfig(object):
    FRONTEND_HOST = None
    FRONTEND_PORT = None
    FRONTEND_RUN_OPTIONS = {}

def create_app(subproject):
    app = Flask(subproject, instance_relative_config=True,
                instance_path=os.environ.get('UKNOW_CONFIG'))
    app.jinja_env.add_extension('pyjade.ext.jinja.PyJadeExtension')
    app.config.from_object(DefaultConfig())
    try:
        app.config.from_pyfile('config.py')
    except IOError:
        # TODO use logging module
        print 'WARNING: No configuration found, using builtin defaults.'
    return app
