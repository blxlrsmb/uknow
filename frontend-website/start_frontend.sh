#!/bin/bash -e
# File: start_frontend.sh
# Date: Wed Nov 13 11:51:54 2013 +0800
# Author: Yuxin Wu <ppwwyyxxc@gmail.com>

PROG_NAME=`readlink -f "$0"`
PROG_DIR=`dirname "$PROG_NAME"`

../manage/exec-in-virtualenv.sh  $PROG_DIR/ukfrontend/app.py
