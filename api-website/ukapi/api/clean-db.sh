#!/bin/bash -e
# File: clean-db.sh
# Date: Thu Dec 12 10:40:30 2013 +0800
# Author: Yuxin Wu <ppwwyyxxc@gmail.com>

if [[ "$1" == "user" ]]; then
	mongo << EOF
use uknow
db.user.remove()
db.fetcher_guokr_rss.remove()
db.global_counter.remove()
EOF
fi
