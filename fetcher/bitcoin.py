#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# File: bitcoin.py
# Date: Sat Mar 23 16:41:41 2013 +0800
# Author: Yuxin Wu <ppwwyyxxc@gmail.com>

from BeautifulSoup import BeautifulSoup
import requests

url = "https://mtgox.com/"

def getPrice():
    ''' return float, in US dollars'''
    r = requests.get(url)
    soup = BeautifulSoup(r.text)
    price = soup.find("li", {"id": "lastPrice"}).first('span').getText()
    return float(price.strip('$ \t'))

if __name__ == '__main__':
    print getPrice()
