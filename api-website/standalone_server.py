#!../manage/exec-in-virtualenv.sh
# -*- coding: utf-8 -*-
# $File: standalone_server.py
# $Date: Tue Nov 12 20:16:29 2013 +0800
# $Author: jiakai <jia.kai66@gmail.com>

from ukapi import get_app

def main():
    get_app().run('0.0.0.0', debug = True)

if __name__ == "__main__":
    main()
