#!../../manage/exec-in-virtualenv.sh
# -*- coding: utf-8 -*-
# $File: texttagger_liblinear.py
# $Date: Sun Dec 22 00:09:03 2013 +0800
# $Author: Xinyu Zhou <zxytim[at]gmail[dot]com>

"""text tagger, used by prefilter"""

import nltk
import operator
import jieba
import html2text
import tfidf
import cPickle as pickle
import re
from liblinear.python.liblinearutil import *

LABLE_PREFIX = u'autotag:'


def _html2text_wo_new_line(html):
    h = html2text.HTML2Text()
    h.ignore_links = True
    h.ignore_images = True
    h.ignore_emphasis = True
    h.ul_item_mark = ''
    h.emphasis_mark = ''
    h.strong_mark = ''

    return re.sub(r'[ \n]+', ' ', h.handle(html))


class TextTagger(object):

    """a text tagger that automatically tag texts"""

    model = None
    tfidf_model = None
    labels_id = None
    labels_dict = dict()

    def __init__(self, nr_min_word_count=0):
        self.nr_min_word_count = nr_min_word_count

    def _filter_words(self, words):
        return filter(lambda w: len(w.rstrip()) > 0, words)

    def _get_document_words(self, doc):
        doc = _html2text_wo_new_line(doc).lower()
        words = self._filter_words(map(
            lambda x: x, jieba.cut(doc, cut_all=True)))
        tokens = self._filter_words(map(
            lambda x: x, jieba.cut(doc, cut_all=False)))
        words.extend(map(lambda x: "".join(x), nltk.bigrams(tokens)))
        words.extend(map(lambda x: "".join(x), nltk.trigrams(tokens)))
        return words

    def fit(self, training_data):
        """:param training_data: a list of tuple, each tuple comprises of
        raw text from database (may contain html code), and its label(s). e.g,
        [('NBA 2k13', ['sports', 'computer']), ('hello world', 'programming')]
        """
        self.tfidf_model = tfidf.TFIDF(self.nr_min_word_count)

        print("training tfidf model ...")
        data_by_words = []
        labels_set = set()
        for doc, labels in training_data:
            words = self._get_document_words(doc)
            if isinstance(labels, basestring):
                labels = [labels]

            for l in labels:
                labels_set.add(l)
                data_by_words.append((words, l))
            self.tfidf_model.add_document(words)

        self.labels_id = list(labels_set)
        self.labels_dict = dict(map(lambda x: (x[1], x[0]),
            enumerate(self.labels_id)))

        self.tfidf_model.shrink_by_df()
        print("#tokens: {}" . format(len(self.tfidf_model.term2id)))
        print("generating feature vector ...")
        y, x = [], []
        for words, label in data_by_words:
            feature_vector = self._get_feature_vector_by_words(words)
            y.append(self.labels_dict[label])
            x.append(dict(feature_vector))

        print("training liblinear ...")
        self.model = train(y, x, '-s 0') # regression

    def _get_feature_vector_by_words(self, words):
        return dict(self.tfidf_model.get_feature_vector(words))

    def predict_one(self, document):
        """:param: document: raw text from database, may contain html code"""
        words = self._get_document_words(document)
        feature_vector = self._get_feature_vector_by_words(words)

        # prob_classify return a distribution
        p_label, p_acc, p_val = predict([0], [feature_vector], self.model,
            '-b 1')
        ave = 1.0 / len(p_val[0])
        model_labels = self.model.get_labels()
        labels = [LABLE_PREFIX + self.labels_id[model_labels[i]] for i in range(len(p_val[0]))
                if p_val[0][i] > ave]
        return labels

    def dump(self, file_name):
        print 'saving liblinear model ...'
        save_model(file_name, self.model)
        print 'saving tfidf model ...'
        with open(file_name + ".tfidf", 'w') as fout:
            pickle.dump(self.tfidf_model, fout)
        print 'saving labels_id ...'
        with open(file_name + ".labels_id", 'w') as fout:
            pickle.dump(self.labels_id, fout)
        print 'saving labels_dict ...'
        with open(file_name + ".labels_dict", 'w') as fout:
            pickle.dump(self.labels_dict, fout)

    @staticmethod
    def load(file_name):
        tagger = TextTagger()
        tagger.model = load_model(file_name)
        with open(file_name + ".tfidf") as fin:
            tagger.tfidf_model = pickle.load(fin)
        with open(file_name + ".labels_id") as fin:
            tagger.labels_id = pickle.load(fin)
        with open(file_name + ".labels_dict") as fin:
            tagger.labels_dict = pickle.load(fin)
        return tagger

def test():
    training_data = [
        ('I love this sandwich.', 'pos'),
        ('This is an amazing place!', 'pos'),
        ('I feel very good about these beers.', 'pos'),
        ('This is my best work.', 'pos'),
        ("What an awesome view", 'pos'),
        ('I do not like this restaurant', 'neg'),
        ('I am tired of this stuff.', 'neg'),
        ("I can't deal with this", 'neg'),
        ('He is my sworn enemy!', 'neg'),
        ('My boss is horrible.', 'neg'),
        (u'天气真不错！', 'pos'),
        (u'天气真糟糕！', 'neg'),
    ]
    test_data = [
        ('The beer was good.', 'pos'),
        ('I do not enjoy my job', 'neg'),
        ("I ain't feeling dandy today.", 'neg'),
        ("I feel amazing!", 'pos'),
        ('Gary is a friend of mine.', 'pos'),
        ("I can't believe I'm doing this.", 'neg'),
        ("can't be good any more", 'pos'),
        (u'你人很不错！', 'pos'),
        (u'这人真糟糕！', 'neg'),
    ]

    tagger = TextTagger()
    tagger.fit(training_data)
    for doc, label in test_data:
        pred = tagger.predict_one(doc)
        print(pred, label)

if __name__ == '__main__':
    test()

# vim: foldmethod=marker
