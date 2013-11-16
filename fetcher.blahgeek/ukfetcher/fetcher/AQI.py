#!/usr/bin/env python2
# -*- coding: utf-8 -*-
# By i@BlahGeek.com at 10/11/2013

from BeautifulSoup import BeautifulSoup
import requests

url = "http://iphone.bjair.info/m/beijing/mobile"


def getBeijingAQI():
    ''' return int '''
    r = requests.get(url)
    soup = BeautifulSoup(r.text)
    return int(soup.first('h1').getText())

if __name__ == '__main__':
    print getBeijingAQI()
