#!/bin/bash
# $File: exec-api-in-virtualenv.sh
# $Date: Thu Oct 17 19:41:06 2013 +0800
# $Author: jiakai <jia.kai66@gmail.com>

dir=$(dirname $0)/api-website/.env

if [ ! -d "$dir" ]
then
	echo "$dir not found; please first run 'quickinstall' for api-website"
	exit
fi

if [ -z "$1" ]
then
	echo "usage: $0 <python script>"
	exit
fi

. $dir/bin/activate

python $1

