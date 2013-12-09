#!/bin/bash -e
# $File: celery_worker.sh
# $Date: Mon Dec 09 12:55:45 2013 +0800
# $Author: jiakai <jia.kai66@gmail.com>

realpath() {
  [[ $1 = /* ]] && echo "$1" || echo "$PWD/${1#./}"
}

if [ `uname` = 'Darwin' ]
then
  PROG_NAME=`realpath "$0"`
else
  PROG_NAME=`readlink -f "$0"`
fi

PROG_DIR=`dirname "$PROG_NAME"`
cd "$PROG_DIR"

. ../manage/setenv.sh

celery --app=celery_app.app worker -l info
