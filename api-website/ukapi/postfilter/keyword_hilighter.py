#!/usr/bin/env python2
# -*- coding: utf-8 -*-
# $File: keyword_hilighter.py
# $Date: Sat Dec 14 22:35:30 2013 +0800
# $Author: jiakai <jia.kai66@gmail.com>

from . import PostfilterBase

import re
import unicodedata


class KeywordHilighter(PostfilterBase):

    @staticmethod
    def _highlight(s):
        return u'<span class="highlight">{}</span>'.format(s.group(0))

    def _get_name(self):
        return 'keyword_hilighter'

    def _get_disp_name(self):
        return u'关键字高亮'

    def _get_config_type(self):
        return ['keywords']

    def enable(self, user_id, config):
        def get_re(s):
            s = s.strip()
            if all(map(lambda i: unicodedata.category(i) != 'Lo', s)):
                s = ur'\b' + s + ur'\b'
            return '(' + s + ')'
        keywords = config['keywords'].lower().split(',')
        re = u'|'.join(map(get_re, keywords))
        self._save_config(user_id, re)

    def disable(self, user_id):
        self._del_config(user_id)

    def apply(self, ctx, docs):
        expr = self._load_config(ctx.user_id)
        reobj = re.compile(expr)
        for i in docs:
            desc = i['desc']
            for name in ['title', 'content']:
                val = getattr(desc, name, None)
                if val:
                    val = reobj.sub(self._highlight, val)
                    setattr(desc, name, val)
