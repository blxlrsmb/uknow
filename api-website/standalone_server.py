#!../manage/exec-in-virtualenv.sh
# -*- coding: utf-8 -*-
# $File: standalone_server.py
# $Date: Wed Nov 13 11:33:04 2013 +0800
# $Author: jiakai <jia.kai66@gmail.com>

from ukapi import get_app

def main():
    app = get_app()
    try:
        app.config.from_pyfile('config.py')
    except IOError:
        print 'WARNING: No configuration found, using builtin defaults.'

    app.run(app.config['API_HOST'], app.config['API_PORT'],
            **app.config['API_RUN_OPTIONS'])

if __name__ == "__main__":
    main()
