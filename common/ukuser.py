#!/usr/bin/env python2
# -*- coding: utf-8 -*-
# $File: ukuser.py
# $Date: Wed Dec 11 17:03:49 2013 +0800
# $Author: jiakai <jia.kai66@gmail.com>

"""utilities for managing users"""


def get_enabled_fetcher(user_id):
    """:return: a list of fetcher names enabled by this user; the fetchers must
    be user type, not general type"""
    return ['sample_user']   # TODO XXX


def get_enabled_prefilter(user_id):
    """:return: a list of prefilter names enabled by this user"""
    return ['sample_user']    # TODO  XXX

# TODO get_enabled_postfilter, user register, user
# authentication, etc.
