#!../exec-api-in-virtualenv.sh
# -*- coding: utf-8 -*-
# $File: standalone_server.py
# $Date: Wed Oct 16 22:31:05 2013 +0800
# $Author: jiakai <jia.kai66@gmail.com>

from ukapi import get_app

def main():
    get_app().run('0.0.0.0', debug = True)

