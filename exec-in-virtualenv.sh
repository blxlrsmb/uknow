#!/bin/bash
# $File: exec-in-virtualenv.sh
# $Date: Fri Oct 11 23:09:17 2013 +0800
# $Author: jiakai <jia.kai66@gmail.com>

dir=$(dirname $0)/.env

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

