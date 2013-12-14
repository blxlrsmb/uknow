#!/usr/bin/env python2
# -*- coding: utf-8 -*-
# $File: util.py
# $Date: Sat Dec 14 19:14:29 2013 +0800
# $Author: jiakai <jia.kai66@gmail.com>

from ukutil import MongoDBSet
import time

_db_set = MongoDBSet('ukfetcher_user_config')


def insert_db_item(user_id, set_name, item_name):
    """insert an item into a set in mongodb"""
    _db_set.add('{}-{}'.format(user_id, set_name), item_name)


def remove_db_item(user_id, set_name, item_name):
    """insert an item into a set in mongodb"""
    _db_set.remove('{}-{}'.format(user_id, set_name), item_name)


def get_db_set(user_id, set_name):
    return _db_set.get('{}-{}'.format(user_id, set_name))
