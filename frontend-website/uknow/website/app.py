# encoding=utf-8
from uknow.utils import create_app
from .apps.base import base


def create_website_app():
    app = create_app('website')
    app.register_blueprint(base)
    return app


def main():
    app = create_website_app()
    app.run(app.config['HOST'], app.config['PORT'],
            **app.config['RUN_OPTIONS'])
