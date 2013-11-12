#!/bin/bash
# $File: celery_worker.sh
# $Date: Wed Nov 13 01:16:23 2013 +0800
# $Author: jiakai <jia.kai66@gmail.com>

. ../manage/setenv.sh

celery --app=celery_app.app worker -l info
