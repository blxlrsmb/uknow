#!../exec-api-in-virtualenv.sh
# -*- coding: utf-8 -*-
# $File: standalone_server.py
# $Date: Thu Oct 17 19:37:09 2013 +0800
# $Author: jiakai <jia.kai66@gmail.com>

from ukapi import get_app

def main():
    get_app().run('0.0.0.0', debug = True)

if __name__ == "__main__":
    main()
