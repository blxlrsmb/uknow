#!../manage/exec-in-virtualenv.sh
# -*- coding: utf-8 -*-
# $File: train_tagger.py
# $Date: Thu Dec 12 20:41:56 2013 +0800
# $Author: Xinyu Zhou <zxytim[at]gmail[dot]com>

"""train tagger from tags in the database"""


import ukconfig
from ukdbconn import get_mongo
from lib.texttagger import TextTagger


def main():
    db = get_mongo('item')
    data = []
    for item in db.find():
        if 'other' in item and item['other'] and 'content' in item['other']:
            labels = item['tag']
            if len(labels) == 0:
                continue
            doc = item['other']['content'][0]['value']
            data.append((doc, labels))

    print("#documents: {}" . format(len(data)))
    print("training ...\n")
    tagger = TextTagger(nr_min_word_count=3)
    tagger.fit(data)
    print("writing model...\n")
    tagger.dump(ukconfig.tagger_path)


if __name__ == '__main__':
    main()

# vim: foldmethod=marker
