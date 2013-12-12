#!/usr/bin/env python2
# -*- coding: utf-8 -*-
# $File: util.py
# $Date: Thu Dec 12 23:13:02 2013 +0800
# $Author: jiakai <jia.kai66@gmail.com>

from flask_login import current_user, login_required


def get_current_user_id():
    return current_user.username
