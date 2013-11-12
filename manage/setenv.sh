#!/bin/bash -e
# $File: setenv.sh
# $Date: Wed Nov 13 01:10:15 2013 +0800
# $Author: jiakai <jia.kai66@gmail.com>

script_dir=$(dirname ${BASH_SOURCE[0]})
source $script_dir/config.sh

project_root=$script_dir/..
env_dir=$project_root/.env

if [ ! -d "$env_dir" ]
then
	echo "$env_dir not found; please first run 'quickinstall'"
	exit
fi

. $env_dir/bin/activate

for i in $modules
do
	PYTHONPATH=$PYTHONPATH:$project_root/$i
done
export PYTHONPATH

