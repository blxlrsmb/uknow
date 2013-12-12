#!/bin/bash -e
# File: test-tab.sh
# Date: Thu Dec 12 11:04:09 2013 +0800
# Author: Yuxin Wu <ppwwyyxxc@gmail.com>
DEST="http://localhost:5000"

if [[ $1 == "login" ]]; then
	curl -X POST -d "{\"username\":\"testuser\", \"password\": \"testpass\" }" \
		-H "Content-Type:application/json" $DEST/login -c 'cookie.txt'
elif [[ $1 == "add" ]]; then
	curl -X POST -d "{\"name\":\"tab2\" }" \
		-H "Content-Type:application/json" $DEST/add_tab -b 'cookie.txt'
elif [[ $1 == "getall" ]]; then
	curl -H "Content-Type:application/json" $DEST/get_all_tabs -b 'cookie.txt'
elif [[ $1 == "del" ]]; then
	curl -H "Content-Type:application/json" "$DEST/del_tab?name=tab1" -b 'cookie.txt'
fi
