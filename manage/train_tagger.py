#!../manage/exec-in-virtualenv.sh
# -*- coding: utf-8 -*-
# $File: train_tagger.py
# $Date: Sat Dec 21 18:42:38 2013 +0800
# $Author: Xinyu Zhou <zxytim[at]gmail[dot]com>

"""train tagger from tags in the database"""


import ukconfig
from ukdbconn import get_mongo, declare_tag
from ukitem import ItemDescBase
from lib.texttagger import TextTagger

import random

MAX_DATA_SIZE = 140


def main():
    db = get_mongo('item')
    data = []
    for item in db.find():
        desc = ItemDescBase.deserialize(item['desc'])
        labels = item['tag']
        if not labels:
            continue
        doc = desc.render_content()
        data.append((doc, labels))
        declare_tag(labels)

    print("#documents: {}" . format(len(data)))
    print("training ...\n")
    random.shuffle(data)
    data = data[:MAX_DATA_SIZE]
    tagger = TextTagger(nr_min_word_count=3)
    tagger.fit(data)
    print("writing model...\n")
    tagger.dump(ukconfig.tagger_path)


if __name__ == '__main__':
    main()

# vim: foldmethod=marker
