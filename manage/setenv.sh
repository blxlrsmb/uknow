#!/bin/bash -e
# $File: setenv.sh
# $Date: Wed Nov 13 02:21:05 2013 +0800
# $Author: jiakai <jia.kai66@gmail.com>

script_dir=$(dirname $0)
source $script_dir/config.sh

project_root=$script_dir/..
env_dir=$project_root/.env

if [ ! -d "$env_dir" ]
then
	echo "$env_dir not found; please first run 'quickinstall'"
fi

. $env_dir/bin/activate


# zsh compatibility
[[ -n $ZSH_VERSION ]] && set -o shwordsplit

for i in $ukmodules
do
	echo $i
	PYTHONPATH=$PYTHONPATH:$project_root/$i
done
export PYTHONPATH

