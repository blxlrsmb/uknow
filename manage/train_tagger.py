#!../manage/exec-in-virtualenv.sh
# -*- coding: utf-8 -*-
# $File: train_tagger.py
# $Date: Sun Dec 22 00:10:18 2013 +0800
# $Author: Xinyu Zhou <zxytim[at]gmail[dot]com>

"""train tagger from tags in the database"""


import ukconfig
from ukdbconn import get_mongo, declare_tag
from ukitem import ItemDescBase
from lib.texttagger import TextTagger
from collections import defaultdict

import random

MAX_DATA_SIZE = 10000


def filter_data_label(data, label_set):
    ret = []
    for x, y in data:
        new_y = [i for i in y if i in label_set]
        ret.append((x, new_y))
    return ret


def main():
    label_cnt = defaultdict(int)
    db = get_mongo('item')
    data = []
    for item in db.find():
        desc = ItemDescBase.deserialize(item['desc'])
        labels = item['tag']
        if not labels:
            continue
        for l in labels:
            label_cnt[l] += 1
        doc = desc.render_content()
        data.append((doc, labels))

    available_labels = set()
    total_cnt = sum(label_cnt.values())
    print total_cnt
    for label, cnt in label_cnt.iteritems():
        if cnt > total_cnt * 0.0015 and cnt < total_cnt * 0.1:
            available_labels.add(label)

    print 'remaining labels: ', len(available_labels)

    print("#documents: {}" . format(len(data)))
    print("training ...\n")
    random.shuffle(data)
    data = data[:MAX_DATA_SIZE]
    data = filter_data_label(data, available_labels)
    tagger = TextTagger(nr_min_word_count=3)
    tagger.fit(data)
    print("writing model...\n")
    tagger.dump(ukconfig.tagger_path)


if __name__ == '__main__':
    main()

# vim: foldmethod=marker
