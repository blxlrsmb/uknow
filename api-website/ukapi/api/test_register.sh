#!/bin/bash -e
# File: test_register.sh
# Date: Tue Dec 10 09:41:29 2013 +0800
# Author: Yuxin Wu <ppwwyyxxc@gmail.com>

DEST="http://localhost:5000"

curl -X POST -d "{\"username\":\"testuser\", \"password\": \"testpass\" }" \
	-H "Content-Type:application/json" $DEST/register
