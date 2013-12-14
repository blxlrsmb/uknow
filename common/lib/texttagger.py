#!../../manage/exec-in-virtualenv.sh
# -*- coding: utf-8 -*-
# $File: texttagger.py
# $Date: Sat Dec 14 16:14:33 2013 +0800
# $Author: Xinyu Zhou <zxytim[at]gmail[dot]com>

"""text tagger, used by prefilter"""

from nltk import NaiveBayesClassifier
import nltk
import operator
import jieba
import html2text
import tfidf
import cPickle as pickle
import re

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

    classifier = None
    tfidf_model = None

    def __init__(self, prob_lower_bound=0.1, relative_threshold=0.95,
                 nr_min_word_count=0):
        """:param: prob_lower_bound: a number between 0 and 1, only take labels
            that has a probability greater than this into account
        :param: relative_threshold: consider all labels that has a probability
            greater than the relative_threshold of maximum probability
        :param: nr_min_word_count: only use words whose number of appearances
            aboves this number"""

        self.prob_lower_bound = prob_lower_bound
        self.relative_threshold = relative_threshold
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
        for doc, labels in training_data:
            words = self._get_document_words(doc)
            if isinstance(labels, basestring):
                labels = [labels]

            for l in labels:
                data_by_words.append((words, l))
            self.tfidf_model.add_document(words)

        self.tfidf_model.shrink_by_df()
        print("#tokens: {}" . format(len(self.tfidf_model.term2id)))
        print("generating feature vector ...")
        data = []
        for words, label in data_by_words:
            feature_vector = self._get_feature_vector_by_words(words)
            data.append((dict(feature_vector), label))

        print("training NaiveBayesClassifier ...")
        self.classifier = NaiveBayesClassifier.train(data)

    def _get_feature_vector_by_words(self, words):
        return dict(self.tfidf_model.get_feature_vector(words))

    def predict_one(self, document):
        """:param: document: raw text from database, may contain html code"""
        words = self._get_document_words(document)
        feature_vector = self._get_feature_vector_by_words(words)

        # prob_classify return a distribution
        dist = self.classifier.prob_classify(feature_vector)
        prob = map(dist.prob, dist.samples())
        ans = zip(dist.samples(), prob)
        max_prob = max(ans, key=operator.itemgetter(1))[1]
        ans = filter(
            lambda x: x[1] > max_prob * self.relative_threshold
            and x[1] > self.prob_lower_bound,
            ans)
        labels = map(operator.itemgetter(0), ans)
        labels = [LABLE_PREFIX + i for i in labels]
        return labels

    def dump(self, file_name):
        with open(file_name, 'w') as fout:
            pickle.dump(self, fout)

    @staticmethod
    def load(file_name):
        with open(file_name) as fin:
            return pickle.load(fin)


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
