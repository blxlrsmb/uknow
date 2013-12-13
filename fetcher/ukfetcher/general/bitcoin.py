#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# File: bitcoin.py
# Date: Fri Dec 13 16:03:51 2013 +0800
# Author: Yuxin Wu <ppwwyyxxc@gmail.com>

from . import register_fetcher
from ukitem import TextOnlyItem
from uklogger import log_fetcher as log_info

from BeautifulSoup import BeautifulSoup
import requests

url = "https://vip.btcchina.com/"


def getPrice():
    ''' return float, in CNY'''
    r = requests.get(url)
    soup = BeautifulSoup(r.text)
    price = soup.find("span", {"id": "last"}).getText()
    return float(price.replace(",", ""))


@register_fetcher('Bitcoin', sleep_time=60)
def bitcoin_fetcher(ctx):
    """fetcher btcchina.com, save with tag `bitcoin`"""
    price = getPrice()
    ctx.new_item(TextOnlyItem("Last Bitcoin Price: " +
                              u"¥" + str(price), ""), ['Bitcoin'])
    log_info(u'bitcoin price update: {}'.format(price))
