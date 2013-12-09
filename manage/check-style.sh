#!/bin/bash -e
# File: check-style.sh
# Date: Sat Nov 16 20:22:24 2013 +0800
# Author: Yuxin Wu <ppwwyyxxc@gmail.com>

[[ -n $ZSH_VERSION ]] && script_dir=$(dirname $0) || script_dir=$(dirname ${BASH_SOURCE[0]})
source $script_dir/setenv.sh

realpath() {
  [[ $1 = /* ]] && echo "$1" || echo "$PWD/${1#./}"
}

if [ `uname` == 'Darwin' ]
then
  real_dir=$(realpath $script_dir)/..
else
  real_dir=$(readlink -f $script_dir)/..
fi


pep8 $real_dir --exclude=.env,.git,fetcher.blahgeek --statistics

