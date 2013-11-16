#!/bin/bash
# $File: gendoc.sh
# $Date: Sat Nov 16 15:54:49 2013 +0800
# $Author: jiakai <jia.kai66@gmail.com>

. ../../manage/setenv.sh

sphinx-apidoc -o source/autogen ../../api-website/ukapi
sphinx-apidoc -o source/autogen ../../fetcher/ukfetcher
sphinx-apidoc -o source/autogen ../../common/

