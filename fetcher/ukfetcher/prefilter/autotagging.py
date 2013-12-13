#!/usr/bin/python2
# -*- coding: utf-8 -*-
# $File: autotagging.py
# $Date: Fri Dec 13 04:56:22 2013 +0800
# $Author: Xinyu Zhou <zxytim[at]gmail[dot]com>

"""auto tagging prefilter"""

from . import prefilter
import ukconfig
from lib.texttagger import TextTagger
from uklogger import log_info

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
    if _tagger and ('other' in doc) and doc['other'] \
            and ('content' in doc['other']):
        content = doc['other']['content']
        if not isinstance(content, basestring):
            if isinstance(content, list):
                content = content[0]
            if isinstance(content, dict):
                if 'value' in content:
                    content = content['value']
                else:
                    return
            else:
                return
        tags = _tagger.predict_one(content)
#        log_info(content)
        log_info('original tag: ' + str(doc['tag']))
        log_info('autotagging: ' + str(tags))
        doc['tag'] = list(set(doc['tag'] + tags))
    """auto tag """

# vim: foldmethod=marker
