#!/usr/bin/env python2
# -*- coding: UTF-8 -*-
# File: bitcoin.py
# Date: Thu Dec 12 20:01:28 2013 +0800
# Author: Yuxin Wu <ppwwyyxxc@gmail.com>

from BeautifulSoup import BeautifulSoup
import requests

url = "https://mtgox.com/"


def getPrice():
    ''' return float, in US dollars'''
    r = requests.get(url)
    soup = BeautifulSoup(r.text)
    print soup
    price = soup.find("li", {"id": "lastPrice"}).first('span').getText()
    return float(price.strip('$ \t'))

if __name__ == '__main__':
    print getPrice()
