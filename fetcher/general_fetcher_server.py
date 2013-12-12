#!../manage/exec-in-virtualenv.sh
# -*- coding: utf-8 -*-
# $File: general_fetcher_server.py
# $Date: Thu Dec 12 21:18:58 2013 +0800
# $Author: jiakai <jia.kai66@gmail.com>

from gevent import monkey
monkey.patch_all()

from ukfetcher.general import start_server


def main():
    start_server()


if __name__ == "__main__":
    main()
