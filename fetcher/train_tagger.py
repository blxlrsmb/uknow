#!../manage/exec-in-virtualenv.sh
# -*- coding: utf-8 -*-
# $File: train_tagger.py
# $Date: Fri Dec 13 11:24:08 2013 +0800
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
            doc = item['other']['content']
            if len(doc) > 0 and 'value' in doc[0]:
                doc = doc[0]['value']
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
