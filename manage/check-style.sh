#!/bin/bash -e
# File: check-style.sh
# Date: Sat Nov 16 20:22:24 2013 +0800
# Author: Yuxin Wu <ppwwyyxxc@gmail.com>

[[ -n $ZSH_VERSION ]] && script_dir=$(dirname $0) || script_dir=$(dirname ${BASH_SOURCE[0]})
source $script_dir/setenv.sh

real_dir=$(readlink -f $script_dir)/..

pep8 $real_dir --exclude=.env,.git,fetcher.blahgeek --statistics

