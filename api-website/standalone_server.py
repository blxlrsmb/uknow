#!../exec-in-virtualenv.sh
# -*- coding: utf-8 -*-
# $File: standalone_server.py
# $Date: Fri Oct 11 22:48:15 2013 +0800
# $Author: jiakai <jia.kai66@gmail.com>

from ukapi import get_app

if __name__ == '__main__':
    get_app().run('0.0.0.0', debug = True)

