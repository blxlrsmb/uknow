#!/bin/bash -e
# $File: setenv.sh
# $Date: Sat Nov 16 20:32:13 2013 +0800
# $Author: jiakai <jia.kai66@gmail.com>

# zsh compatibility when direct sourcing from shell
[[ -n $ZSH_VERSION ]] && script_dir=$(dirname $0) || script_dir=$(dirname ${BASH_SOURCE[0]})
source $script_dir/config.sh

project_root=$(readlink -f $script_dir/..)
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
	PYTHONPATH=$PYTHONPATH:$project_root/$i
done
export PYTHONPATH=$PYTHONPATH:$project_root

export UKNOW_CONFIG=$(readlink -f $script_dir)

