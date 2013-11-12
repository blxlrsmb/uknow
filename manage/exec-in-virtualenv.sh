#!/bin/bash -e
# $File: exec-in-virtualenv.sh
# $Date: Wed Nov 13 00:56:30 2013 +0800
# $Author: jiakai <jia.kai66@gmail.com>

# start a python script in virtualenv, with appropriate envrionment variables
# set

source $(dirname $0)/setenv.sh

if [ -z "$1" ]
then
	echo "usage: $0 <python script>"
	exit
fi

python $1

