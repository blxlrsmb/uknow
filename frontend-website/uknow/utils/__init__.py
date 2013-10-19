import os
import os.path

from flask import Flask


class DefaultConfig(object):
    HOST = None
    PORT = None
    RUN_OPTIONS = {}
    DEBUG = True


def create_app(subproject):
    app = Flask('uknow.%s' % subproject, instance_relative_config=True,
                instance_path=os.environ.get('uknow_INSTANCE'))
    app.jinja_env.add_extension('pyjade.ext.jinja.PyJadeExtension')
    app.config.from_object(DefaultConfig())
    try:
        app.config.from_pyfile(os.path.join('config', '%s.py' % subproject))
    except IOError:
        # TODO use logging module
        print 'WARNING: No configuration found, using builtin defaults.'
    return app
