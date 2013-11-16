#!/usr/bin/env python2
# -*- coding: utf-8 -*-
# $File: uklogger.py
# $Date: Tue Nov 12 22:39:00 2013 +0800
# $Author: jiakai <jia.kai66@gmail.com>

"""utilities for handling logging"""

import traceback


def log_info(msg):
    """log an info message"""
    print 'INFO', msg
    # TODO: use log util, log to file, including time, module, etc.


def log_err(msg):
    """log an err message"""
    print 'ERR', msg


def log_exc(exc):
    """log an unexpected exception"""
    log_info('Caught unexpected exception: {}\n{}'.format(
        exc, traceback.format_exc()))
