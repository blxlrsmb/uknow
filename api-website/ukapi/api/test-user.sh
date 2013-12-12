#!/bin/bash -e
# File: test-user.sh
# Date: Fri Dec 13 02:41:15 2013 +0800
# Author: Yuxin Wu <ppwwyyxxc@gmail.com>

DEST="http://localhost:5000"

if [[ $1 == "register" ]]; then
	curl -v "$DEST/register?username=testuser&password=testpass"
elif [[ $1 == "login" ]]; then
	curl -v "$DEST/login?username=testuser&password=testpass" -c cookie.txt
elif [[ $1 == "logout" ]]; then
	curl -v -H "Content-Type:application/json" $DEST/logout -b 'cookie.txt' -c 'cookie.txt'
fi
