#!/bin/bash -e
# File: clean-db.sh
# Date: Wed Dec 11 21:41:10 2013 +0800
# Author: Yuxin Wu <ppwwyyxxc@gmail.com>

if [[ "$1" == "user" ]]; then
	mongo << EOF
use uknow
db.user.remove()
db.global_counter.remove({'_id': 'n_user'})
EOF
fi
