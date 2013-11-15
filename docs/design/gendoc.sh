#!/bin/bash
# $File: gendoc.sh
# $Date: Fri Nov 15 20:51:22 2013 +0800
# $Author: jiakai <jia.kai66@gmail.com>

. ../../manage/setenv.sh

sphinx-apidoc -o source/autogen ../../api-website/ukapi
sphinx-apidoc -o source/autogen ../../fetcher/ukfetcher

