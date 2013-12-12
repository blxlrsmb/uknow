#!/bin/bash -e
# File: clean-db.sh
# Date: Thu Dec 12 11:34:58 2013 +0800
# Author: Yuxin Wu <ppwwyyxxc@gmail.com>

mongo << EOF
use uknow
db.user.remove()
db.fetcher_guokr_rss.remove()
db.item.remove()
db.global_counter.remove()
EOF
