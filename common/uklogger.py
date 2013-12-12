#!/usr/bin/env python2
# -*- coding: utf-8 -*-
# $File: uklogger.py
# $Date: Thu Dec 12 19:32:51 2013 +0800
# $Author: jiakai <jia.kai66@gmail.com>

"""utilities for handling logging"""

import traceback
from termcolor import cprint


def log_api(msg):
    """log a message from api-website"""
    cprint('API: ' + msg, 'green')
    # TODO: use log util, log to file, including time, module, etc.


def log_fetcher(msg):
    """log a message from fetcher"""
    cprint('API: ' + msg, 'yellow')
    # TODO: use log util, log to file, including time, module, etc.


def log_info(msg):
    """log an info message"""
    cprint('INFO: ' + msg, 'blue')
    # TODO: use log util, log to file, including time, module, etc.


def log_err(msg):
    """log an err message"""
    cprint('INFO: ' + msg, 'red', attrs=['blink'])
    # TODO: use log util, log to file, including time, module, etc.


def log_exc(exc):
    """log an unexpected exception"""
    log_err('Caught unexpected exception: {}\n{}'.format(
        exc, traceback.format_exc()))
