#!/bin/bash -e
# File: test-user.sh
# Date: Thu Dec 12 14:31:18 2013 +0800
# Author: Yuxin Wu <ppwwyyxxc@gmail.com>

DEST="http://localhost:5000"

if [[ $1 == "register" ]]; then
	curl -v -X POST -d "{\"username\":\"testuser\", \"password\": \"testpass\" }" \
		-H "Content-Type:application/json" $DEST/register
elif [[ $1 == "login" ]]; then
	curl -v -X POST -d "{\"username\":\"testuser\", \"password\": \"testpass\" }" \
		-H "Content-Type:application/json" $DEST/login -c 'cookie.txt'
elif [[ $1 == "logout" ]]; then
	curl -v -H "Content-Type:application/json" $DEST/logout -b 'cookie.txt' -c 'cookie.txt'
fi
