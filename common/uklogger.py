#!/usr/bin/env python2
# -*- coding: utf-8 -*-
# $File: uklogger.py
# $Date: Sat Dec 14 18:03:00 2013 +0800
# $Author: jiakai <jia.kai66@gmail.com>

"""utilities for handling logging"""

import traceback
from termcolor import colored

from ukutil import is_in_unittest


def log_api(msg):
    """log a message from api-website"""
    print colored('API', 'green'), msg
    # TODO: use log util, log to file, including time, module, etc.


def log_fetcher(msg):
    """log a message from fetcher"""
    print colored('FETCHER', 'yellow'), msg
    # TODO: use log util, log to file, including time, module, etc.


def log_info(msg):
    """log an info message"""
    print colored('INFO', 'blue'), msg
    # TODO: use log util, log to file, including time, module, etc.


def log_err(msg):
    """log an err message"""
    print colored('ERR', 'red', attrs=['blink']), msg
    # TODO: use log util, log to file, including time, module, etc.


def log_exc(exc):
    """log an unexpected exception"""
    log_err('Caught unexpected exception: {}\n{}'.format(
        exc, traceback.format_exc()))

if is_in_unittest():
    log_api = log_fetcher = log_info = lambda msg: None
