#!/bin/bash -e
if [ $# -lt 3 ]
then
  echo "usage: $0 requests concurrency url"
  exit 0
fi
REQUESTS=$1
CONCURRENCY=$2
URL=$3
OUTPUTDIR=output
PLOT=gnuplot
TITLE="$REQUESTS-$CONCURRENCY-$URL"
LOG="$TITLE.log"
FIGURE="$TITLE.png"
COMMAND="ab -k -n $REQUESTS -c $CONCURRENCY -g $OUTPUTDIR/$LOG $3/"

mkdir -p $OUTPUTDIR
bash -c "$COMMAND"
$PLOT -e "set terminal png;set output '$FIGURE';set title 'Response Time for $URL with $CONCURRENCY in Parallel';set size 1,0.7;set grid y;set xlabel 'request';set ylabel 'response time (ms)';plot '$OUTPUTDIR/$LOG' using 9 smooth sbezier with lines title '$URL'"
