#!/bin/bash -e
# File: test-tag.sh
# Date: Thu Dec 12 11:54:36 2013 +0800
# Author: Yuxin Wu <ppwwyyxxc@gmail.com>
DEST="http://localhost:5000"

if [[ $1 == "login" ]]; then
	curl -X POST -d "{\"username\":\"testuser\", \"password\": \"testpass\" }" \
		-H "Content-Type:application/json" $DEST/login -c 'cookie.txt'
elif [[ $1 == "add" ]]; then
	curl -X POST -d "{\"name\":\"guokr\", \"tab\": \"tab2\" }" \
		-H "Content-Type:application/json" $DEST/add_tag -b 'cookie.txt'
elif [[ $1 == "getall" ]]; then
	curl -H "Content-Type:application/json" $DEST/get_all_tags -b 'cookie.txt'
elif [[ $1 == "del" ]]; then
	curl -H "Content-Type:application/json" "$DEST/del_tag?name=guokr&tab=tab1" -b 'cookie.txt'
elif [[ $1 == "del2" ]]; then
	curl -H "Content-Type:application/json" "$DEST/del_tag?name=guokr&tab=tab2" -b 'cookie.txt'
fi