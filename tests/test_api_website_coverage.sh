#!/bin/bash

set -x
function count_down {
	for i in `seq $1 -1 1`; do
		echo test will be start in $i seconds
		sleep 1
	done
}

REPORT_DIR=api_webiste_coverage_test_report
BROWSER=chromium

source ../manage/setenv.sh

python2 -m coverage run ../api-website/standalone_server.py > /tmp/test_api_website.log &
SERVER_PID=$!

count_down 5

./test_api_website.py
RET_VAL=$?
kill -s SIGINT $SERVER_PID
[ "x$RET_VAL" != "x0" ] && exit 1

python2 -m coverage html --omit="*.env/*" -d $REPORT_DIR
python2 -m coverage erase
$BROWSER $REPORT_DIR/index.html
