#!/bin/bash -e
# File: test-tab.sh
# Date: Wed Dec 11 21:34:10 2013 +0800
# Author: Yuxin Wu <ppwwyyxxc@gmail.com>
DEST="http://localhost:5000"

if [[ $1 == "add" ]]; then
	curl -X POST -d "{\"name\":\"tab1\" }" \
		-H "Content-Type:application/json" $DEST/add_tab -b 'cookie.txt'
elif [[ $1 == "getall" ]]; then
	curl -H "Content-Type:application/json" $DEST/get_all_tabs -b 'cookie.txt'
elif [[ $1 == "logout" ]]; then
	curl -H "Content-Type:application/json" $DEST/logout -b 'cookie.txt' -c 'cookie.txt'
fi
