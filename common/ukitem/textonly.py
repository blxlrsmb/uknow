#!/usr/bin/env python2
# -*- coding: utf-8 -*-
# $File: textonly.py
# $Date: Fri Dec 13 15:01:13 2013 +0800
# $Author: jiakai <jia.kai66@gmail.com>


from .base import ItemDescBase
from ukutil import ensure_unicode

import cPickle as pickle


class TextOnlyItem(ItemDescBase):
    title = None
    content = None

    def __init__(self, title, content):
        self.title = ensure_unicode(title)
        self.content = ensure_unicode(content)

    def _do_serialize(self):
        title = self.title.encode('utf-8')
        content = self.content.encode('utf-8')
        return pickle.dumps((title, content), pickle.HIGHEST_PROTOCOL)

    @classmethod
    def _do_deserialize(cls, data):
        title, content = pickle.loads(data)
        return cls(title, content)

    @staticmethod
    def get_desc_name():
        return 'textonly'

    def render_title(self):
        return u'{}'.format(self.title)

    def render_content(self):
        return u'{}'.format(self.content)
