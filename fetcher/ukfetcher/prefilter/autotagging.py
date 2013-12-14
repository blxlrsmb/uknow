#!/usr/bin/python2
# -*- coding: utf-8 -*-
# $File: autotagging.py
# $Date: Sat Dec 14 16:08:38 2013 +0800
# $Author: Xinyu Zhou <zxytim[at]gmail[dot]com>

"""auto tagging prefilter"""

from . import prefilter
from uklogger import log_info
from lib.texttagger import TextTagger
import ukconfig

_tagger = None


@prefilter('auto_tag')
def auto_tagging(ctx, doc):
    """auto tagging an item.
        It will load tagger model from `ukconfig.tagger_path`.
        Model should be trained prior to make this function work"""
    global _tagger
    if _tagger is None:
        try:
            log_info('loading tagger ...')
            _tagger = TextTagger.load(ukconfig.tagger_path)
        except IOError:
            log_info('tagger model not found.')
            return

    tags = _tagger.predict_one(doc['desc'].content)
    log_info('original tag: ' + str(doc['tag']))
    log_info('autotagging: ' + str(tags))
    doc['tag'] = list(set(doc['tag'] + tags))
    """auto tag """

# vim: foldmethod=marker
