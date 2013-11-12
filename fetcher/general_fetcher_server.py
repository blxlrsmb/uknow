#!../manage/exec-in-virtualenv.sh
# -*- coding: utf-8 -*-
# $File: general_fetcher_server.py
# $Date: Wed Nov 13 01:01:24 2013 +0800
# $Author: jiakai <jia.kai66@gmail.com>

from gevent import monkey
monkey.patch_all()

from ukfetcher.general import start_server

start_server()
