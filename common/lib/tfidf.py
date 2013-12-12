#!/usr/bin/python2
# -*- coding: utf-8 -*-
# $File: tfidf.py
# $Date: Thu Dec 12 21:43:02 2013 +0800
# $Author: Xinyu Zhou <zxytim[at]gmail[dot]com>

import pickle
import math
from collections import defaultdict


class TFIDF:
    def __init__(self, nthres):
        self.NTHRES = int(nthres)
        self._df = defaultdict(int)  # term -> doc freq
        self.term2id = dict()
        self.nd = 0  # number of doc
        self.log_nd = 0

    # a document is a list of words
    def add_document(self, document):
        self.nd += 1
        self.log_nd = math.log(self.nd)
        for t in document:
            if t not in self.term2id:
                self.term2id[t] = len(self.term2id)
            self._df[t] += 1

    def dump(self, fname):
        self.shrink_by_df()
        with open(fname, 'w') as fout:
            pickle.dump(self, fout)

    def dumps(self):
        self.shrink_by_df()
        return pickle.dumps(self)

    def shrink_by_df(self):
        newdf = defaultdict(int)
        for k, v in self._df.iteritems():
            if v > self.NTHRES:
                newdf[k] = v
        self._df = newdf
        self.term2id = dict()
        cnt = 1
        for term in self._df.iterkeys():
            self.term2id[term] = cnt
            cnt += 1

    @staticmethod
    def load(fname):
        with open(fname) as fin:
            return pickle.load(fin)

    # a smooth wrapper for get df without add new item in dict
    def df(self, t):
        ret = 1
        if t in self._df:
            ret += self._df[t]
        return ret

    # return: term -> tf
    def get_tf(self, document):
        ret = defaultdict(int)
        for t in document:
            ret[t] += 1
        return ret

    def get_feature_vector(self, document):
        """return: [(key_0, val_0), (key_1, val_1), ...], key start from 1"""
        ret = []
        tfs = self.get_tf(document)
        for t, tf in tfs.iteritems():
            # a term that does not appear in corpus does not contribute
            if t not in self.term2id:
                continue
            key = self.term2id[t]
            idf = math.log(self.nd) - math.log(self.df(t))
            val = (1 + math.log(tf)) * idf
            ret.append((key + 1, val))

        return sorted(ret)


# vim: foldmethod=marker
