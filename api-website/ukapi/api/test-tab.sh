#!/bin/bash -e
# File: test-tab.sh
# Date: Thu Dec 12 20:04:28 2013 +0800
# Author: Yuxin Wu <ppwwyyxxc@gmail.com>
DEST="http://localhost:5000"

if [[ $1 == "login" ]]; then
	curl -v "$DEST/login?username=testuser&password=testpass" -c cookie.txt
elif [[ $1 == "add" ]]; then
	curl -X POST -d "{\"name\":\"tab1\", \"priority\": 1 }" \
		-H "Content-Type:application/json" $DEST/add_tab -b 'cookie.txt'
	curl -X POST -d "{\"name\":\"tab2\", \"priority\": 1 }" \
		-H "Content-Type:application/json" $DEST/add_tab -b 'cookie.txt'
elif [[ $1 == "getall" ]]; then
	curl -H "Content-Type:application/json" $DEST/get_all_tabs -b 'cookie.txt'
elif [[ $1 == "get" ]]; then
	curl -H "Content-Type:application/json" "$DEST/get_tab_article?tab=tab1" -b 'cookie.txt'
elif [[ $1 == "del" ]]; then
	curl -H "Content-Type:application/json" "$DEST/del_tab?name=tab1" -b 'cookie.txt'
fi
