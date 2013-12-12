#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# File: bitcoin.py
# Date: Thu Dec 12 20:32:13 2013 +0800
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


@register_fetcher('bitcoin', sleep_time=60)
def bitcoin_fetcher(ctx):
    """fetcher btcchina.com, save with tag `bitcoin`"""
    price = getPrice()
    ctx.new_item(TextOnlyItem("Last Bitcoin Price",
                              "¥" + str(price)), ['bitcoin'])
    log_info(u'bitcoin price update: {}'.format(price))
