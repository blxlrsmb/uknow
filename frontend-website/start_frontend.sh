#!/bin/bash -e
# File: start_frontend.sh
# Date: Wed Nov 13 11:51:54 2013 +0800
# Author: Yuxin Wu <ppwwyyxxc@gmail.com>

realpath() {
  [[ $1 = /* ]] && echo "$1" || echo "$PWD/${1#./}"
}

if [ `uname` == 'Darwin' ]
then
  PROG_NAME=`realpath "$0"`
else
  PROG_NAME=`readlink -f "$0"`
fi
PROG_DIR=`dirname "$PROG_NAME"`

../manage/exec-in-virtualenv.sh  $PROG_DIR/ukfrontend/app.py
