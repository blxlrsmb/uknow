#!/usr/bin/env python2
# -*- coding: utf-8 -*-
# $File: ukuser.py
# $Date: Wed Nov 13 01:34:23 2013 +0800
# $Author: jiakai <jia.kai66@gmail.com>

"""utilities for managing users"""


def get_enabled_fetcher(user_id):
    """:return: a list of fetcher names enabled by this user"""
    return ['sample_user', 'guokr_rss']   # TODO XXX


def get_enabled_prefilter(user_id):
    """:return: a list of prefilter names enabled by this user"""
    return ['sample_user']    # TODO  XXX

# TODO get_enabled_postfilter, user register, user
# authentication, etc.
