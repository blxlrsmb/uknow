#!/bin/bash
# $File: exec-in-virtualenv.sh
# $Date: Wed Oct 16 22:30:51 2013 +0800
# $Author: jiakai <jia.kai66@gmail.com>

dir=$(dirname $0)/api-website/.env

if [ ! -d "$dir" ]
then
	echo "$dir not found; please first install virtualenv for python2 there"
	exit
fi

if [ -z "$1" ]
then
	echo "usage: $0 <python script>"
	exit
fi

. $dir/bin/activate

python $1

