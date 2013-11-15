#!/bin/bash
# $File: gendoc.sh
# $Date: Fri Nov 15 20:26:19 2013 +0800
# $Author: jiakai <jia.kai66@gmail.com>

. ../../manage/setenv.sh

sphinx-apidoc2 -o source/autogen ../../api-website/ukapi

