#!/bin/bash

REPORT_DIR=api_webiste_coverage_test_report
BROWSER=chromium

export IN_UKNOW_TEST=1

function count_down {
	for i in `seq $1 -1 1`; do
		echo test will start in $i seconds
		sleep 1
	done
}


source ../manage/setenv.sh

python -m coverage run ../api-website/standalone_server.py 2> server_log &
SERVER_PID=$!

count_down 5

python -m unittest -v testcase.api_website
RET_VAL=$?

kill -s SIGINT $SERVER_PID

python -m coverage html \
	--include="*manage/config,*api-website*,*" \
	--omit="*common/lib*,*.env*,*ukfetcher/general*,*uklogger*" \
	-d $REPORT_DIR
python -m coverage erase
$BROWSER $REPORT_DIR/index.html

wait $SERVER_PID || (echo 'server failed!'; cat server_log)
[ "x$RET_VAL" != "x0" ] && exit 1
