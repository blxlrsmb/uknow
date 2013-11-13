#!/bin/bash -e
# $File: celery_worker.sh
# $Date: Wed Nov 13 11:52:47 2013 +0800
# $Author: jiakai <jia.kai66@gmail.com>


PROG_NAME=`readlink -f "$0"`
PROG_DIR=`dirname "$PROG_NAME"`
cd "$PROG_DIR"

. ../manage/setenv.sh

celery --app=celery_app.app worker -l info
