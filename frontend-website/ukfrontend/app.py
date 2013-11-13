# encoding=utf-8
from utils import create_app
from apps.base import base


def create_website_app():
    app = create_app('ukfrontend')
    app.register_blueprint(base)
    return app


def main():
    app = create_website_app()
    app.run(app.config['FRONTEND_HOST'], app.config['FRONTEND_PORT'],
            **app.config['FRONTEND_RUN_OPTIONS'])

if __name__ == "__main__":
    main()
